from PySide import QtGui, QtCore
import ujson
import sys
import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends import qt_compat
import shutil
import webbrowser
import data_io
import appdirs


from scalable_mw import Ui_MainWindow

from text_file_viewer import Ui_Dialog

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE

if hasattr(sys, 'frozen') and sys.platform == 'darwin':
    print "Detected a frozen application and extracting the appropriate file directory format"
    base_directory = os.path.join(os.path.dirname(sys.executable))
else:
    base_directory = '.'


user_data_directory = appdirs.user_data_dir("CarbonXS_GUI")



if use_pyside:
    from PySide.QtCore import *
    from PySide.QtGui import *

class FittingParams(object):
    # Fitting Parameters object to store current FPs in buffer

    def __init__(self, parameter_list, param_enable, fit_settings, diff_settings):

        self.param_values = [param.value() for param in parameter_list]

        self.param_flags = [pe.isChecked() for pe in param_enable]

        self.fit_settings = {}
        for key in fit_settings.keys():
            if key == 'number_layers':
                self.fit_settings[key] = fit_settings[key].currentIndex()
            else:
                self.fit_settings[key] = fit_settings[key].value()

        self.diff_values = [ds.value() for ds in diff_settings]


class TextFileViewer(QtGui.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        """
        Text File Viewer

        Displays the contents of a text file so that the user may specify 

        :param parent:
        """


        super(TextFileViewer, self).__init__(parent)
        self.setupUi(self)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.setWindowTitle('Load a Text File')

    def load_contents(self, filename):
        text = open(filename).read()
        self.text_display.setPlainText(text)

class ConsoleStream(QtCore.QObject):

    message = QtCore.Signal(str)
    def __init__(self, parent=None):

        super(ConsoleStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, version):

        """
        Initializes the main window of the program
        :param version: String to use in the window header indicating the program version
        """



        super(MainWindow, self).__init__()

        self.version = version

        self.setupUi(self)


        self.parameter_list = [
            self.param_00,
            self.param_01,
            self.param_02,
            self.param_03,
            self.param_04,
            self.param_05,
            self.param_06,
            self.param_07,
            self.param_08,
            self.param_09,
            self.param_10,
            self.param_11,
            self.param_12,
            self.param_13,
            self.param_14,
            self.param_15,
            self.param_16,
            self.param_17,
        ]

        for item in self.parameter_list:
            item.setMaximum(1e21)
            item.setMinimum(-1e21)
            item.setDecimals(5)

        self.parameter_labels = [
            self.param_label_00,
            self.param_label_01,
            self.param_label_02,
            self.param_label_03,
            self.param_label_04,
            self.param_label_05,
            self.param_label_06,
            self.param_label_07,
            self.param_label_08,
            self.param_label_09,
            self.param_label_10,
            self.param_label_11,
            self.param_label_12,
            self.param_label_13,
            self.param_label_14,
            self.param_label_15,
            self.param_label_16,
            self.param_label_17,
        ]

        self.parameter_enable_list = [
            self.param_enable_00,
            self.param_enable_01,
            self.param_enable_02,
            self.param_enable_03,
            self.param_enable_04,
            self.param_enable_05,
            self.param_enable_06,
            self.param_enable_07,
            self.param_enable_08,
            self.param_enable_09,
            self.param_enable_10,
            self.param_enable_11,
            self.param_enable_12,
            self.param_enable_13,
            self.param_enable_14,
            self.param_enable_15,
            self.param_enable_16,
            self.param_enable_17,
        ]


        self.fit_settings = {'theta_min':self.theta_min_value,
                             'theta_max':self.theta_max_value,
                             'iterations':self.iterations,
                             'epsilon':self.epsilon,
                             'nskip':self.nskip,
                             'number_layers':self.number_layers,
                             'tci_pts':self.n_phi,
                             'integration_width':self.n_sg
                             }

        self.diff_settings = [self.wavelength, self.sample_depth, self.sample_width,
                              self.goniometer_radius, self.beam_width, self.sample_density]

        self.num_params = len(self.parameter_list)

        self.init_ui_elements()

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.x_data = []
        self.y_data = []
        self.x_fit_data = []
        self.y_fit_data = []
        self.prev_x_fit = []
        self.prev_y_fit = []

        self.ax.tick_params(axis='both', which='major', labelsize=14)
        self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
        self.ax.grid(True)
        self.addmpl(self.fig)

        self.y_axis_lim = None
        self.x_axis_lim = None

        self.current_filename = None

        # Remember the last header lines / separator used
        self.last_header_lines_used = 0
        self.last_separator_used = 0


        # Default data directories
        self.default_diff_data_dir = None
        self.default_export_dir = None
        self.default_carboninp_import_dir = None
        self.default_carboninp_export_dir = None
        self.default_fitparams_import_dir = None
        self.default_fitparams_export_dir = None
        self.default_fitsettings_import_dir = None
        self.default_fitsettings_export_dir = None
        self.default_diffsettings_import_dir = None
        self.default_diffsettings_export_dir = None

        # Fitting Process
        self.fitting_process = QtCore.QProcess(self)
        self.fitting_process.readyRead.connect(self.on_process_message)
        self.fitting_process.finished.connect(self.fitting_finished)
        self.pattern_calc_flag = False
        self.abort_flag = False

        self.init_menubar_osx()
        self.assignWidgets()
        self.setWindowTitle("CarbonXS GUI v"+version)
        self.showMaximized()

        # Undo Buffer
        self.append_to_buffer = True
        self.undo_buffer = []
        self.undo_index = 0

        QtGui.QFontDatabase.addApplicationFont(os.path.join(base_directory, 'fonts', 'SourceCodePro-Regular.ttf'))
        console_font = QtGui.QFont()
        console_font.setFamily('Source Code Pro')
        self.console.setFont(console_font)




    def write_config(self):

        """
        Exports the current program configuration to JSON
        
        
        :return: 
        """

        configuration = {'program_config':
                             {'last_header_lines':self.last_header_lines_used,
                              'last_separator':self.last_separator_used,
                              'lock_x':bool(self.lock_x_axis.checkState()),
                              'lock_y':bool(self.lock_y_axis.checkState()),
                              'show_previous_fit':bool(self.show_previous.checkState()),

                              },
                          'file_defaults':
                              {'diff_data_dir':self.default_diff_data_dir,
                               'export_dir':self.default_export_dir,
                               'export_carboninp':self.default_carboninp_export_dir,
                               'import_carboninp':self.default_carboninp_import_dir,
                               'export_fitparams':self.default_fitparams_export_dir,
                               'import_fitparams':self.default_fitparams_import_dir,
                               'export_fitsettings':self.default_fitsettings_export_dir,
                               'import_fitsettings':self.default_fitsettings_import_dir,
                               'export_diffsettings':self.default_diffsettings_export_dir,
                               'import_diffsettings':self.default_diffsettings_import_dir,


                              }

                         }

        config_file = open(os.path.join(user_data_directory, 'config','config.json'), 'w')

        ujson.dump(configuration, config_file, indent=4)


    def first_time_app_setup(self):

        """
        Sets up the directory structure into the user data directories
        
        Returns
        -------

        """

        print "Running first time app data setup."
        print "Creating data directory in %s"%user_data_directory
        if not os.path.exists(user_data_directory):
            os.makedirs(user_data_directory)
        if not os.path.exists(os.path.join(user_data_directory, "config")):
            os.mkdir(os.path.join(user_data_directory, "config"))
        if not os.path.exists(os.path.join(user_data_directory, "config", 'diffractometer settings')):
            os.mkdir(os.path.join(user_data_directory, "config", 'diffractometer settings'))
            shutil.copy2(os.path.join(base_directory, 'config','diffractometer settings',
                                      'dal_diffractometer.json'),
                         os.path.join(user_data_directory, 'config', 'diffractometer settings'))
            shutil.copy2(os.path.join(base_directory, 'config','diffractometer settings',
                                      'unm_diffractometer.json'),
                         os.path.join(user_data_directory, 'config', 'diffractometer settings'))

        if not os.path.exists(os.path.join(user_data_directory, "config", 'fitting parameters')):
            os.mkdir(os.path.join(user_data_directory, "config", 'fitting parameters'))
            shutil.copy2(os.path.join(base_directory, 'config','fitting parameters',
                                      'example_params.json'),
                         os.path.join(user_data_directory, 'config', 'fitting parameters'))
        if not os.path.exists(os.path.join(user_data_directory, "config", 'fitting settings')):
            os.mkdir(os.path.join(user_data_directory, "config", 'fitting settings'))
            shutil.copy2(os.path.join(base_directory, 'config','fitting settings',
                                      'example_settings.json'),
                         os.path.join(user_data_directory, 'config', 'fitting settings'))
        if not os.path.exists(os.path.join(user_data_directory, "examples")):
            os.mkdir(os.path.join(user_data_directory, "examples"))
            shutil.copy2(os.path.join(base_directory, 'examples','CARBON.INP'),
                         os.path.join(user_data_directory, 'examples'))
            shutil.copy2(os.path.join(base_directory, 'examples','crystalline_carbon.dat'),
                         os.path.join(user_data_directory, 'examples'))


    def data_init(self):
        """"
        On startup, read the last used Carbon.INP file
        """

        if not os.path.exists(user_data_directory):
            self.first_time_app_setup()


        # Attempts to load a Carbon.INP file if it exists
        try:
            self.read_carboninp(os.path.join(base_directory, 'carbonxs', 'carbon.inp'))

            print "Loaded most recently used parameters successfully from 'carbonxs' directory."
        except IOError:
            print "No previous parameters found in 'carbonxs' directory."

        # Clears any SCAN.DAT file already in carbonxs directory
        if 'SCAN.DAT' in os.listdir(os.path.join(base_directory, 'carbonxs')):
            os.remove(os.path.join(base_directory, 'carbonxs', 'SCAN.DAT'))

        # Read in the previously written configuration file
        if 'config.json' in os.listdir(os.path.join(user_data_directory, 'config')):
            config_file = open(os.path.join(user_data_directory, 'config', 'config.json'),'r')
            config = ujson.load(config_file)

            try:
                self.lock_y_axis.setChecked(config['program_config']['lock_y'])
            except KeyError:
                print "No configuration found for Y Axis Lock in config.json. Setting to default of False."
                self.lock_y_axis.setChecked(False)

            try:
                self.lock_x_axis.setChecked(config['program_config']['lock_x'])
            except KeyError:
                print "No configuration found for X Axis Lock in config.json. Setting to default of False."
                self.lock_x_axis.setChecked(False)

            try:
                self.show_previous.setChecked(config['program_config']['show_previous_fit'])
            except KeyError:
                print "No configuration found for Show Previous in config.json. Setting to default of False."
                self.show_previous.setChecked(False)

            try:
                self.last_separator_used = config['program_config']['last_separator']
            except KeyError:
                print "No configuration found for Last Separator Type used. Defaulting to Whitespace"
                self.last_separator_used = 0

            try:
                self.last_header_lines_used = config['program_config']['last_header_lines']
            except KeyError:
                print "No configuration found for Last Number of Header Lines used. Defaulting to 0 Header Lines"
                self.last_header_lines_used = 0

            # Loads file directory defaults from configuration file

            try:
                self.default_diff_data_dir = config['file_defaults']['diff_data_dir']
            except KeyError:
                print "No configuration found for default diffraction data directory. Using default directory."
                self.default_diff_data_dir = None

            try:
                self.default_export_dir = config['file_defaults']['export_dir']
            except KeyError:
                print "No configuration found for default export data directory. Using default directory."
                self.default_export_dir = None

            try:
                self.default_carboninp_export_dir = config['file_defaults']['export_carboninp']
            except KeyError:
                print "No configuration found for default carbon.inp export directory. Using default directory."
                self.default_carboninp_export_dir = None
            try:
                self.default_carboninp_import_dir = config['file_defaults']['import_carboninp']
            except KeyError:
                print "No configuration found for default carbon.inp import directory. Using default directory."
                self.default_carboninp_import_dir = None


            try:
                self.default_fitparams_export_dir = config['file_defaults']['export_fitparams']
            except KeyError:
                print "No configuration found for default fit parameters export directory. Using default directory."
                self.default_fitparams_export_dir = None
            try:
                self.default_fitparams_import_dir = config['file_defaults']['import_fitparams']
            except KeyError:
                print "No configuration found for default fit parameters import directory. Using default directory."
                self.default_fitparams_import_dir = None

            try:
                self.default_fitsettings_export_dir = config['file_defaults']['export_fitsettings']
            except KeyError:
                print "No configuration found for default fit settings export directory. Using default directory."
                self.default_fitsettings_export_dir = None
            try:
                self.default_fitsettings_import_dir = config['file_defaults']['import_fitsettings']
            except KeyError:
                print "No configuration found for default fit settings import directory. Using default directory."
                self.default_fitsettings_import_dir = None

            try:
                self.default_diffsettings_export_dir = config['file_defaults']['export_diffsettings']
            except KeyError:
                print "No configuration found for default diffractometer settings export directory. Using default directory."
                self.default_diffsettings_export_dir = None
            try:
                self.default_diffsettings_import_dir = config['file_defaults']['import_diffsettings']
            except KeyError:
                print "No configuration found for default diffractometer settings import directory. Using default directory."
                self.default_diffsettings_import_dir = None



        self.check_pt_parameter()
        self.check_undo_index()

    def check_pt_parameter(self):
        """
        Depending on the model used, parameter 15 is overloaded to be 2 variables:

                1 layer model - g / Fraction of Low Strain Carbon
                2 layer model - Pt / Probability of 3R stacking


        :return:
        """

        if self.number_layers.currentIndex() == 0:
            self.param_label_15.setText('g, Fraction of Low Strain Carbon')
            print "Currently using 1 layer model - Parameter 15 is g, Fraction of Low Strain Carbon."
        else:
            self.param_label_15.setText('Pt, Probability of 3R Stacking')
            print "Currently using 2 layer model - Parameter 15 is Pt, Probability of 3R Stacking."


    def init_menubar_osx(self):

        """
        Re-initializes the menubar for OSX to make it appear at the top of the screen.
        
        :return: 
        """

        if sys.platform == 'darwin':
            self.menubar = QtGui.QMenuBar()
            self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 21))
            self.menubar.setNativeMenuBar(True)
            self.menubar.setObjectName("menubar")
            self.menu_file = QtGui.QMenu(self.menubar)
            self.menu_file.setObjectName("menu_file")
            self.menu_category_import = QtGui.QMenu(self.menu_file)
            self.menu_category_import.setObjectName("menu_category_import")
            self.menuExport = QtGui.QMenu(self.menu_file)
            self.menuExport.setObjectName("menuExport")
            self.menuFitting = QtGui.QMenu(self.menubar)
            self.menuFitting.setObjectName("menuFitting")
            self.menuHelp = QtGui.QMenu(self.menubar)
            self.menuHelp.setObjectName("menuHelp")
            self.setMenuBar(self.menubar)
            self.menu_open_xrd_pattern = QtGui.QAction(self)
            self.menu_open_xrd_pattern.setObjectName("menu_open_xrd_pattern")
            self.menu_import_carboninp = QtGui.QAction(self)
            self.menu_import_carboninp.setObjectName("menu_import_carboninp")
            self.menu_import_diffsettings = QtGui.QAction(self)
            self.menu_import_diffsettings.setObjectName("menu_import_diffsettings")
            self.menu_import_fittingparams = QtGui.QAction(self)
            self.menu_import_fittingparams.setObjectName("menu_import_fittingparams")
            self.menu_import_fittingsettings = QtGui.QAction(self)
            self.menu_import_fittingsettings.setObjectName("menu_import_fittingsettings")
            self.menu_export_carboninp = QtGui.QAction(self)
            self.menu_export_carboninp.setObjectName("menu_export_carboninp")
            self.menu_export_diffsettings = QtGui.QAction(self)
            self.menu_export_diffsettings.setObjectName("menu_export_diffsettings")
            self.menu_export_fittingparams = QtGui.QAction(self)
            self.menu_export_fittingparams.setObjectName("menu_export_fittingparams")
            self.menu_export_fittingsettings = QtGui.QAction(self)
            self.menu_export_fittingsettings.setObjectName("menu_export_fittingsettings")
            self.menu_calculate_pattern = QtGui.QAction(self)
            self.menu_calculate_pattern.setObjectName("menu_calculate_pattern")
            self.menu_start_fit = QtGui.QAction(self)
            self.menu_start_fit.setObjectName("menu_start_fit")
            self.menu_abort_fit = QtGui.QAction(self)
            self.menu_abort_fit.setObjectName("menu_abort_fit")
            self.menu_tutorial = QtGui.QAction(self)
            self.menu_tutorial.setObjectName("menu_tutorial")
            self.menu_bugreport = QtGui.QAction(self)
            self.menu_bugreport.setObjectName("menu_bugreport")
            self.menu_about = QtGui.QAction(self)
            self.menu_about.setObjectName("menu_about")
            self.menu_exit = QtGui.QAction(self)
            self.menu_exit.setObjectName("menu_exit")
            self.menu_category_import.addAction(self.menu_import_carboninp)
            self.menu_category_import.addAction(self.menu_import_fittingparams)
            self.menu_category_import.addAction(self.menu_import_fittingsettings)
            self.menu_category_import.addAction(self.menu_import_diffsettings)
            self.menuExport.addAction(self.menu_export_carboninp)
            self.menuExport.addAction(self.menu_export_fittingparams)
            self.menuExport.addAction(self.menu_export_fittingsettings)
            self.menuExport.addAction(self.menu_export_diffsettings)
            self.menu_file.addAction(self.menu_open_xrd_pattern)
            self.menu_file.addAction(self.menu_category_import.menuAction())
            self.menu_file.addAction(self.menuExport.menuAction())
            self.menu_file.addAction(self.menu_exit)
            self.menuFitting.addAction(self.menu_calculate_pattern)
            self.menuFitting.addAction(self.menu_start_fit)
            self.menuFitting.addAction(self.menu_abort_fit)
            self.menuHelp.addAction(self.menu_tutorial)
            self.menuHelp.addAction(self.menu_bugreport)
            self.menuHelp.addAction(self.menu_about)
            self.menubar.addAction(self.menu_file.menuAction())
            self.menubar.addAction(self.menuFitting.menuAction())
            self.menubar.addAction(self.menuHelp.menuAction())
            self.retranslateUi(self)


    def init_ui_elements(self):
        """
        Initiates the toolbar buttons

        :return:
        """




        self.open_pattern_button = QtGui.QAction(QtGui.QIcon(os.path.join(base_directory,'icons','open.png')), 'Open Pattern', self)
        self.open_pattern_button.setStatusTip('Open Pattern')
        self.open_pattern_button.setToolTip("Opens a new XRD pattern.")

        self.calculate_pattern_button= QtGui.QAction(QtGui.QIcon(os.path.join(base_directory,'icons','calculator.png')), 'Calculate', self)
        self.calculate_pattern_button.setStatusTip('Calculate Pattern')
        self.calculate_pattern_button.setToolTip("Calculates pattern using current parameters without performing a fit.")

        self.fit_pattern_button= QtGui.QAction(QtGui.QIcon(os.path.join(base_directory,'icons','fit.png')), 'Fit', self)
        self.fit_pattern_button.setStatusTip('Fit Pattern')
        self.fit_pattern_button.setToolTip("Uses current parameters to perform a fit.")

        self.abort_fit_button= QtGui.QAction(QtGui.QIcon(os.path.join(base_directory,'icons','stop.png')), 'Abort', self)
        self.abort_fit_button.setStatusTip('Abort Fit')
        self.abort_fit_button.setEnabled(False)
        self.abort_fit_button.setToolTip("Aborts current fit by killing CarbonXS process.")

        self.export_fit_button= QtGui.QAction(QtGui.QIcon(os.path.join(base_directory,'icons','export.png')), 'Export Last Fit', self)
        self.export_fit_button.setStatusTip('Export Last Fit')
        self.export_fit_button.setToolTip("Export the carbon.out, carbon.dat, and new CARBON.INP files of the most recent fit run by CarbonXS.")

        self.back_button = QtGui.QAction(QtGui.QIcon(os.path.join(base_directory,'icons','back_button.png')), 'Previous Fit/Calc', self)
        self.back_button.setStatusTip('Go to Previous Fit or Calculation')
        self.back_button.setToolTip("Go to Previous Fit or Calculation")

        self.forward_button = QtGui.QAction(QtGui.QIcon(os.path.join(base_directory,'icons','forward_button.png')), 'Next Fit/Calc', self)
        self.forward_button.setStatusTip('Go to Next Fit or Calculation')
        self.forward_button.setToolTip("Go to Next Fit or Calculation")



        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(self.open_pattern_button)
        self.toolbar.addAction(self.calculate_pattern_button)
        self.toolbar.addAction(self.fit_pattern_button)
        self.toolbar.addAction(self.abort_fit_button)
        self.toolbar.addAction(self.export_fit_button)
        self.toolbar.addAction(self.back_button)
        self.toolbar.addAction(self.forward_button)

        # Any time the layer model changes, update the Pt parameter
        self.number_layers.currentIndexChanged.connect(self.check_pt_parameter)


    @QtCore.Slot(str)
    def on_stream_message(self, message):
        """
        Method for reading print messages and error messages that are sent to the console
        :param message:
        :return:
        """


        self.console.moveCursor(QtGui.QTextCursor.End)
        self.console.insertPlainText(message)
        self.console.moveCursor(QtGui.QTextCursor.End)

    def on_process_message(self):
        """
        Method for reading messages from the carbonxs.exe process

        :return:
        """

        self.console.moveCursor(QtGui.QTextCursor.End)

        message = str(self.fitting_process.readAll())
        self.console.insertPlainText(message)
        self.console.moveCursor(QtGui.QTextCursor.End)

        # if a singular matrix is detected raise the option to abort the fit.
        if "Singular matrix." in message:
            reply = QtGui.QMessageBox.critical(self, 'Singular matrix detected.',
                                               "Singular matrix detected. Abort?", QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

            if reply == QtGui.QMessageBox.Yes:
                self.abort_fit_process()



    def addmpl(self, fig):
        """
        Add a Matplotlib object to the plot

        :param fig:
        :return:
        """


        self.canvas = FigureCanvas(fig)
        self.canvas.setMinimumHeight(100)

        self.mplvl.addWidget(self.canvas, 2, 0)
        self.canvas.draw()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        self.mplvl.addWidget(self.mpl_toolbar)



        self.plot_buttons_layout = QtGui.QHBoxLayout()
        self.plot_pattern_button = QtGui.QPushButton(self)
        self.plot_pattern_button.setText("Pattern + Last Fit")
        self.plot_pattern_button.setToolTip("Plots the currently loaded pattern and the last fit result.")

        self.plot_difference_button = QtGui.QPushButton(self)
        self.plot_difference_button.setText("Last Fit Difference")
        self.plot_difference_button.setToolTip("Plots the difference between source and fit data for the last fit result.")

        self.lock_y_axis = QtGui.QCheckBox(self)
        self.lock_y_axis.setText("Lock Pattern/Fit Y-Axis")
        self.lock_y_axis.setToolTip("Locks the Y-Axis during pattern/fit plotting.")

        self.lock_x_axis = QtGui.QCheckBox(self)
        self.lock_x_axis.setText("Lock Pattern/Fit X-Axis")
        self.lock_x_axis.setToolTip("Locks the X-Axis during pattern/fit plotting.")

        self.show_previous = QtGui.QCheckBox(self)
        self.show_previous.setText("Show Previous Fit")
        self.show_previous.setToolTip("Shows the Previous Iteration's Fit Result")

        self.plot_buttons_layout.addWidget(self.plot_pattern_button)
        self.plot_buttons_layout.addWidget(self.plot_difference_button)

        self.plot_buttons_layout.addWidget(self.lock_y_axis)
        self.plot_buttons_layout.addWidget(self.lock_x_axis)
        self.plot_buttons_layout.addWidget(self.show_previous)



        self.mplvl.addLayout(self.plot_buttons_layout)



    def assignWidgets(self):
        """
        Assigns buttons and menu items to functions

        :return:
        """




        # Toolbar buttons
        self.open_pattern_button.triggered.connect(self.open_pattern)
        self.calculate_pattern_button.triggered.connect(lambda: self.calculate_pattern(append_to_buffer=True))
        self.fit_pattern_button.triggered.connect(self.start_fitting_process)
        self.abort_fit_button.triggered.connect(self.abort_fit_process)
        self.export_fit_button.triggered.connect(self.export_fit_results)
        self.back_button.triggered.connect(self.go_back)
        self.forward_button.triggered.connect(self.go_forward)

        # Enable/Disable/Invert All Parameter Buttons
        self.enable_all_button.clicked.connect(self.enable_all_params)
        self.enable_none_button.clicked.connect(self.disable_all_params)
        self.enable_invert_button.clicked.connect(self.invert_all_params)
        self.enable_bg_button.clicked.connect(self.enable_background_params)


        # self.import_data.clicked.connect(self.load_parameters)
        self.menu_open_xrd_pattern.triggered.connect(self.open_pattern)
        self.menu_import_carboninp.triggered.connect(self.import_from_carboninp)
        self.menu_import_diffsettings.triggered.connect(self.import_diffractometer_params)
        self.menu_import_fittingparams.triggered.connect(self.import_fitting_params)
        self.menu_import_fittingsettings.triggered.connect(self.import_fitting_settings)
        self.menu_exit.triggered.connect(self.close)

        # Export Data
        self.menu_export_carboninp.triggered.connect(self.export_to_carboninp)
        self.menu_export_diffsettings.triggered.connect(self.export_diffractometer_params)
        self.menu_export_fittingparams.triggered.connect(self.export_fitting_params)
        self.menu_export_fittingsettings.triggered.connect(self.export_fitting_settings)

        # Fitting Process Options
        self.menu_calculate_pattern.triggered.connect(lambda: self.calculate_pattern(append_to_buffer=True))
        self.menu_start_fit.triggered.connect(self.start_fitting_process)
        self.menu_abort_fit.triggered.connect(self.abort_fit_process)

        # Graph buttons
        self.plot_pattern_button.clicked.connect(self.plot_loaded_data)
        self.plot_difference_button.clicked.connect(self.plot_difference)

        # Help Menu
        self.menu_tutorial.triggered.connect(self.open_documentation)
        self.menu_bugreport.triggered.connect(self.open_bug_report_page)
        self.menu_about.triggered.connect(self.open_about_dialog)

        self.set_shortcut_keys()



    def set_shortcut_keys(self):
        """
        Sets the shortcut keys for widgets
        :return: 
        """

        self.menu_open_xrd_pattern.setShortcut(QtGui.QKeySequence.Open)
        self.menu_tutorial.setShortcut(QtGui.QKeySequence.HelpContents)
        self.menu_calculate_pattern.setShortcut(Qt.CTRL+Qt.Key_R)
        self.menu_start_fit.setShortcut(Qt.CTRL+Qt.SHIFT+Qt.Key_R)
        self.menu_abort_fit.setShortcut(Qt.CTRL+Qt.Key_D)
        self.back_button.setShortcut(QtGui.QKeySequence.Back)
        self.forward_button.setShortcut(QtGui.QKeySequence.Forward)

        if 'win32' in sys.platform:
            self.menu_exit.setShortcut(Qt.ALT+Qt.Key_F4)
        else:
            self.menu_exit.setShortcut(QtGui.QKeySequence.Quit)

        self.open_pattern_button.setToolTip(self.open_pattern_button.toolTip()+" (%s)"%QtGui.QKeySequence.toString(QtGui.QKeySequence(QtGui.QKeySequence.Open),
                                                                                                                 format=QKeySequence.NativeText))
        self.calculate_pattern_button.setToolTip(self.calculate_pattern_button.toolTip()+" (%s)"%QtGui.QKeySequence.toString(QtGui.QKeySequence(Qt.CTRL+Qt.Key_R),
                                                                                                                           format=QKeySequence.NativeText))
        self.fit_pattern_button.setToolTip(self.fit_pattern_button.toolTip()+" (%s)"%QtGui.QKeySequence.toString(QtGui.QKeySequence(Qt.CTRL+Qt.SHIFT+Qt.Key_R),
                                                                                                                           format=QKeySequence.NativeText))
        self.abort_fit_button.setToolTip(self.abort_fit_button.toolTip()+" (%s)"%QtGui.QKeySequence.toString(QtGui.QKeySequence(Qt.CTRL+Qt.Key_D),
                                                                                                             format=QKeySequence.NativeText))
        self.back_button.setToolTip(self.back_button.toolTip()+" (%s)"%QtGui.QKeySequence.toString(QtGui.QKeySequence(QtGui.QKeySequence.Back),
                                                                                                         format=QKeySequence.NativeText))
        self.forward_button.setToolTip(self.forward_button.toolTip()+" (%s)"%QtGui.QKeySequence.toString(QtGui.QKeySequence(QtGui.QKeySequence.Forward),
                                                                                                    format=QKeySequence.NativeText))


    def plot_difference(self):

        """
        Loads the current carbon.dat and plots the difference between source and fit data.

        :return:
        """

        if len(self.x_data) == 0:

            reply = QtGui.QMessageBox.information(self, 'Warning',
                                              "No pattern data loaded. Cannot calculate a difference.",
                                              QtGui.QMessageBox.Close)

            return


        pattern_filename = os.path.join(base_directory, 'carbonxs', 'carbon.dat')

        self.x_fit_data = []
        self.y_fit_data = []



        fit_color = "#fc8d62"
        pattern_file = open(pattern_filename, 'r')
        for line in pattern_file.readlines():
            data_elements = line.split()
            self.x_fit_data.append(float(data_elements[0]))
            self.y_fit_data.append(float(data_elements[2]))

        interpolated_y_data = np.interp(np.array(self.x_data), np.array(self.x_fit_data), np.array(self.y_fit_data))

        self.fig.clf()
        self.ax_diff = self.fig.add_subplot(111)
        self.ax_diff.plot(self.x_data, np.array(self.y_data) - interpolated_y_data, label="Source - Fit", linewidth = 2, color=fit_color)

        self.ax_diff.ticklabel_format(style='sci', scilimits=(-3,4), axis='y')
        self.ax_diff.tick_params(axis='both', which='major', labelsize=14)
        self.ax_diff.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax_diff.set_ylabel(r'Intensity / a.u.', fontsize=14)


        if self.current_filename:
            self.ax_diff.set_title("Difference - %s"%self.current_filename)
        else:
            self.ax_diff.set_title("Difference")


        self.ax_diff.legend(fontsize=14, frameon=True)
        self.ax_diff.grid(True)
        self.canvas.draw()



    def disable_all_params(self):
        """
        Turns off all fitting parameters
        :return:
        """

        for setting in self.parameter_enable_list:
            setting.setChecked(False)

    def enable_all_params(self):
        """
        Turns on all fitting parameters
        :return:
        """

        for setting in self.parameter_enable_list:
            setting.setChecked(True)

    def invert_all_params(self):
        """
        Inverts all fitting parameters. Enabled becomes disabled and disabled becomes enabled.
        :return:
        """

        for setting in self.parameter_enable_list:
            setting.setChecked(not setting.isChecked())

    def enable_background_params(self):
        """
        Enables only the fitting parameters for the background.
        :return:
        """


        for index, setting in enumerate(self.parameter_enable_list):

            if index > 0 and index < 7:
                setting.setChecked(True)
            else:
                setting.setChecked(False)



    def open_pattern(self):

        """
        Method to call up a file dialog and ask the user to load an XRD pattern
        :return:
        """

        if self.default_diff_data_dir:

            full_path, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.default_diff_data_dir)
        else:
            full_path, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', user_data_directory)


        previous_filename = self.current_filename

        if full_path:
            input_file = open(full_path, 'r')

            directory, filename = os.path.split(full_path)
            if full_path.endswith('.mdi'):

                try:
                    print "Attempting to load MDI file: %s"%full_path
                    self.x_data, self.y_data = data_io.read_mdi_file(full_path)


                    self.current_filename = filename

                    self.default_diff_data_dir = directory

                except ValueError:
                    print "Error: Improperly formatted pattern file in file %s."%full_path
                    print "The pattern file should conform to the JADE MDI format."


                    self.current_filename = previous_filename

                    return

            elif full_path.endswith('.ras'):

                try:
                    print "Attempting to load RAS file: %s"%full_path
                    self.x_data, self.y_data = data_io.read_ras_file(full_path)

                    self.current_filename = filename
                    self.default_diff_data_dir = directory

                except ValueError:
                    print "Error: Improperly formatted pattern file in file %s."%full_path
                    print "The pattern file should conform to the RAS format."

                    self.current_filename = previous_filename
                    return


            else:
                # Pops up dialog with
                loadtxt_dialog = TextFileViewer(self)
                loadtxt_dialog.load_contents(full_path)
                loadtxt_dialog.header_lines.setValue(self.last_header_lines_used)
                loadtxt_dialog.separator_selector.setCurrentIndex(self.last_separator_used)
                header_dialog_accepted = loadtxt_dialog.exec_()
                header_lines = 0

                if header_dialog_accepted:
                    header_lines = loadtxt_dialog.header_lines.value()
                    separator_selection = loadtxt_dialog.separator_selector.currentIndex()

                    if separator_selection == 1:
                        separator = ','
                    elif separator_selection == 0:
                        separator = None

                    else:
                        print "Some other separator not currently implemented is selected"



                else:
                    # User cancelled
                    self.current_filename = previous_filename
                    return

                if header_lines:
                    print "Skipping first %d lines as header."%header_lines
                print "Attempting to load data from text file: %s"%full_path

                try:
                    if separator:
                        plot_data = np.loadtxt(input_file, skiprows=header_lines, delimiter=separator)
                    else:
                        plot_data = np.loadtxt(input_file, skiprows=header_lines)

                    self.x_data = plot_data[:, 0]
                    self.y_data = plot_data[:, 1]
                    self.theta_min_value.setValue(np.min(self.x_data))
                    self.theta_max_value.setValue(np.max(self.x_data))
                    self.current_filename = filename

                    self.last_header_lines_used = header_lines
                    self.last_separator_used = separator_selection
                    self.default_diff_data_dir = directory

                except ValueError:
                    print "Error: loading data from %s"%full_path
                    print "Please check that the number of header lines and the separator is correct."

                    self.current_filename = previous_filename
                    return

            data_pts = len(self.x_data)
            if data_pts > 3000:


                    new_dps = data_pts
                    divisor = 1
                    while new_dps > 3000:
                        divisor += 1
                        new_dps = data_pts / divisor

                    if divisor == 2:
                        divisor_str = '2nd'
                    elif divisor == 3:
                        divisor_str = '3rd'
                    else:
                        divisor_str = "%d th"%divisor


                    reply = QtGui.QMessageBox.warning(self, 'Too many data points.',
                                                       "CarbonXS cannot process > 3000 data points. Do you want to truncate to every %s point?"%divisor_str, QtGui.QMessageBox.Yes |
                                                       QtGui.QMessageBox.No, QtGui.QMessageBox.No)

                    if reply == QtGui.QMessageBox.Yes:

                        self.x_data = self.x_data[0::divisor]
                        self.y_data = self.y_data[0::divisor]

                        new_length = len(self.x_data)
                        print "Data reduced from %d data points to %s data points by taking every %s point."%(data_pts, new_length, divisor_str)

                    else:

                        print "Warning: CarbonXS cannot process datasets larger than 3000 data points and will not fit the full pattern."

            self.plot_loaded_data()

    def plot_fit_results(self):
        """
        Load the most recently generated carbon.dat file and plot the fit results

        :return:
        """
        pattern_filename = os.path.join(base_directory, 'carbonxs', 'carbon.dat')

        self.prev_x_fit = self.x_fit_data
        self.prev_y_fit = self.y_fit_data

        self.x_fit_data = []
        self.y_fit_data = []

        pattern_file = open(pattern_filename, 'r')

        for line in pattern_file.readlines():
            data_elements = line.split()
            self.x_fit_data.append(float(data_elements[0]))
            self.y_fit_data.append(float(data_elements[2]))

        # colors = sns.color_palette('Set2', 2)
        self.plot_loaded_data()

    def calculate_background(self, x_array):
        """
        Calculate Background
        
        Calculates the background of the fit
        
        :param x_array: 
        :return: 
        """


        wavelength = self.wavelength.value()


        # Converts X array into S space using S = 2*sin(x/360 deg)/lambda
        s_array = 2*np.sin(np.array(x_array)*np.pi/(360))/wavelength

        # Grabs the background parameter values
        bg_const = self.parameter_list[1].value()
        bg_1 = self.parameter_list[2].value()
        bg_2 = self.parameter_list[3].value()
        bg_3 = self.parameter_list[4].value()
        bg_4 = self.parameter_list[5].value()
        bg_5 = self.parameter_list[6].value()

        # Calculates the background

        bg = bg_const + bg_1*s_array + bg_2*np.power(s_array, 2.0) + bg_3*np.power(s_array, 3.0)+ bg_4*np.power(s_array, 4.0)
        bg += bg_5*np.power(s_array, -1.0)

        return bg


    def plot_loaded_data(self):
        """
        Plots the loaded source and fit data

        :return:
        """

        source_color = "#66c2a5"
        fit_color = "#fc8d62"
        prev_color = "#8da0cb"
        bg_color = '#e78ac3'




        # If the lock y axis option is enabled, preserve the current axis limits
        # However, only do this if there is already some data that has been plotted
        if len(self.x_fit_data) > 0 or len(self.x_data) > 0:

            if self.lock_y_axis.checkState():
                self.y_limit = self.ax.get_ylim()
            if self.lock_x_axis.checkState():
                self.x_limit = self.ax.get_xlim()

        self.fig.clf()
        self.ax = self.fig.add_subplot(111)

        if len(self.x_data) > 0:
            self.ax.plot(self.x_data, self.y_data, label="Source", linewidth = 2, color=source_color)
        if len(self.x_fit_data) > 0:

        
            background = self.calculate_background(self.x_fit_data)

            self.ax.plot(self.x_fit_data, self.y_fit_data, label="Fit", linewidth = 2, color=fit_color)
            self.ax.plot(self.x_fit_data, background, label="Background", linewidth = 2, color=bg_color)


        if len(self.prev_x_fit) > 0 and self.show_previous.checkState():
            self.ax.plot(self.prev_x_fit, self.prev_y_fit,'--', label="Previous Fit", linewidth = 2, color=prev_color)



        self.ax.tick_params(axis='both', which='major', labelsize=14)
        self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
        if self.current_filename:
            self.ax.set_title("Fit Pattern - %s"%self.current_filename)
        else:
            self.ax.set_title("Fit Pattern")

        self.ax.set_yscale('log')
        self.ax.legend(fontsize=14, frameon=True)
        self.ax.grid(True)

        if self.lock_y_axis.checkState():
            self.ax.set_ylim(self.y_limit)

        if self.lock_x_axis.checkState():
            self.ax.set_xlim(self.x_limit)

        self.canvas.draw()



    def export_diffractometer_params(self):
        """
        Exports currently loaded diffractometer files to a JSON file
        The default directory is "/config/diffractometer settings"

        :return:
        """

        if self.default_diffsettings_export_dir:

            fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export File',
                                                              self.default_diffsettings_export_dir, filter="*.json")
        else:
            fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export File',
                                                          os.path.join(user_data_directory,
                                                          'config', 'diffractometer settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')
            directory, _ = os.path.split(fname)
            self.default_diffsettings_export_dir = directory

            diffractometer_settings = {"wavelength":self.wavelength.value(),
                                       "beam_width":self.beam_width.value(),
                                       "sample_width":self.sample_width.value(),
                                       "sample_depth":self.sample_depth.value(),
                                       "sample_density":self.sample_density.value(),
                                       "gonio_radius":self.goniometer_radius.value(),


                                       }


            ujson.dump(diffractometer_settings, data_file, indent = 4)

            print 'Exported Diffractometer Settings to: %s'%fname
            self.statusBar().showMessage('Exported Diffractometer Settings to: %s'%fname)



    def import_diffractometer_params(self):
        """
        Imports diffractometer files from a JSON file
        The default directory is "/config/diffractometer settings"

        :return:
        """

        if self.default_diffsettings_import_dir:

            fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Export Diffractometer Settings',
                                                              self.default_diffsettings_import_dir, filter="*.json")
        else:

            fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Export Diffractometer Settings',
                                                          os.path.join(user_data_directory,
                                                           'config','diffractometer settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'r')
            directory, _ = os.path.split(fname)
            self.default_diffsettings_import_dir = directory

            try:
                diffractometer_settings = ujson.load(data_file)

                self.wavelength.setValue(diffractometer_settings['wavelength'])
                self.beam_width.setValue(diffractometer_settings['beam_width'])
                self.sample_width.setValue(diffractometer_settings['sample_width'])
                self.sample_depth.setValue(diffractometer_settings['sample_depth'])
                self.sample_density.setValue(diffractometer_settings['sample_density'])
                self.goniometer_radius.setValue(diffractometer_settings['gonio_radius'])

                print 'Imported Diffractometer Settings from: %s'%fname

                self.statusBar().showMessage('Imported Diffractometer Settings from: %s'%fname)

            except ValueError:
                print "Error in loading JSON file: %s."%(fname)
                print "Verify that the configuration file is properly formatted."

            except KeyError:
                import_type = 'diffractometer settings'
                print 'Error in importing %s from: %s.'%(import_type, fname)
                print 'Verify that this settings file is the right kind for this import.'


    def export_fitting_params(self):
        """
        Exports currently loaded fitting parameters files to a JSON file
        The default directory is "/config/fitting parameters"

        :return:
        """

        if self.default_fitparams_export_dir:

            fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export Fitting Parameters',
                                                              self.default_fitparams_export_dir, filter="*.json")
        else:
            fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export Fitting Parameters',
                                                          os.path.join(user_data_directory,
                                                         'config', 'fitting parameters'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')

            directory, _ = os.path.split(fname)
            self.default_fitparams_export_dir = directory

            fitting_params = {}

            for index, label in enumerate(self.parameter_labels):

                fitting_params[label.text()] = (self.parameter_list[index].value(), self.parameter_enable_list[index].isChecked())

            # Include the number of layers used in this model with the fitting parameters export
            fitting_params['number_layers'] = self.number_layers.currentIndex()+1


            ujson.dump(fitting_params, data_file, indent = 4)

            print 'Exported Fitting Parameters to: %s'%fname
            self.statusBar().showMessage('Exported Fitting Parameters to: %s'%fname)

    def import_fitting_params(self):
        """
        Imports fitting parameters files from a JSON file
        The default directory is "/config/fitting parameters"

        :return:
        """

        if self.default_fitparams_import_dir:

            fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Parameters',
                                                              self.default_fitparams_import_dir, filter="*.json")
        else:
            fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Parameters',
                                                          os.path.join(user_data_directory,
                                                                       'config','fitting parameters'), filter="*.json")

        if fname:

            try:
                data_file = open(fname, 'r')
                directory, _ = os.path.split(fname)

                self.default_fitparams_import_dir = directory

                fitting_params = ujson.load(data_file)


                for index, label in enumerate(self.parameter_labels):

                    if ("g, Fraction of Low Strain Carbon" == label.text()
                        or "Pt, Probability of 3R Stacking" == label.text()):


                        # Handle possibility that the
                        if "g, Fraction of Low Strain Carbon" in fitting_params.keys():
                            param_value, enabled = fitting_params["g, Fraction of Low Strain Carbon"]



                        elif "Pt, Probability of 3R Stacking" in fitting_params.keys():
                            param_value, enabled = fitting_params["Pt, Probability of 3R Stacking"]

                        else:
                            print "Could not find parameter 15"
                            param_value = 0
                            enabled = False

                    else:
                        param_value, enabled = fitting_params[label.text()]


                    self.parameter_list[index].setValue(param_value)
                    self.parameter_enable_list[index].setChecked(enabled)




                print 'Imported Fitting Parameters from: %s'%fname
                self.statusBar().showMessage('Imported Fitting Parameters from: %s'%fname)
                errors, warnings = self.check_fitting_parameters()


                # Check if the 1-layer model or 2 layer model encoded into the fitting params JSON file
                # is consistent with currently loaded system
                if 'number_layers' in fitting_params.keys():

                    if self.number_layers.currentIndex() != fitting_params['number_layers']-1:
                        print "Warning: Parameters loaded from a %d layer model system. Current model is a %d layer model."%(fitting_params['number_layers'],
                                                                                                                             self.number_layers.currentIndex()+1)
                        warnings += 1
                
                if errors+warnings > 0:
                    print "Found %d errors and %d warnings. Please ensure parameters are physically meaningful."%(errors, warnings)


            except ValueError:
                print "Error in loading JSON file: %s."%(fname)
                print "Verify that the configuration file is properly formatted."

            except KeyError:
                import_type = 'fitting parameters'
                print 'Error in importing %s from: %s.'%(import_type, fname)
                print 'Verify that this settings file is the right kind for this import.'

    def export_fitting_settings(self):

        """
        Exports currently loaded fitting settings files to a JSON file
        The default directory is "/config/fitting settings"

        :return:
        """

        if self.default_fitsettings_export_dir:
             fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export Fitting Settings',
                                                         self.default_fitsettings_export_dir, filter="*.json")

        else:
            fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export Fitting Settings',
                                                          os.path.join(user_data_directory,
                                                        'config', 'fitting settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')
            directory, _ = os.path.split(fname)
            self.default_fitsettings_export_dir = directory

            fitting_settings = {}

            fitting_settings['theta min'] = self.theta_min_value.value()
            fitting_settings['theta max'] = self.theta_max_value.value()

            fitting_settings['iterations'] = self.iterations.value()
            fitting_settings['nskip']  = self.nskip.value()

            if self.number_layers.currentIndex() == 0:
                fitting_settings['layers'] = 1
            else:
                fitting_settings['layers'] = 2

            fitting_settings['nphi']  = self.n_phi.value()
            fitting_settings['nsg']  = self.n_sg.value()
            fitting_settings['epsilon'] = self.epsilon.value()

            fitting_settings['enable_gc'] = False
            fitting_settings['gc_delta']  = 0
            ujson.dump(fitting_settings, data_file, indent = 4)

            print 'Exported Fitting Settings to: %s'%fname
            self.statusBar().showMessage('Exported Fitting Settings to: %s'%fname)

    def import_fitting_settings(self):

        """
        Import fitting settings from a JSON file
        The default directory is "/config/fitting settings"

        :return:
        """

        if self.default_fitsettings_import_dir:

            fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Settings',
                                                              self.default_fitsettings_import_dir, filter="*.json")
        else:
            fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Settings',
                                                           os.path.join(user_data_directory, 'config',
                                                                        'fitting settings'), filter="*.json")

        if fname:

            try:
                data_file = open(fname, 'r')
                directory, _ = os.path.split(fname)
                self.default_fitsettings_import_dir = directory

                fitting_settings = ujson.load(data_file)

                self.theta_min_value.setValue(fitting_settings['theta min'])
                self.theta_max_value.setValue(fitting_settings['theta max'])

                self.iterations.setValue(fitting_settings['iterations'])
                self.nskip.setValue(fitting_settings['nskip'])


                if fitting_settings['layers'] == 1:
                    self.number_layers.setCurrentIndex(0)
                elif fitting_settings['layers'] == 2:
                    self.number_layers.setCurrentIndex(1)
                else:
                    print "Error: Number of layers is not 1 or 2. Setting it to 1."
                    self.number_layers.setCurrentIndex(0)

                self.n_phi.setValue(fitting_settings['nphi'])
                self.n_sg.setValue(fitting_settings['nsg'])
                self.epsilon.setValue(fitting_settings['epsilon'])

                print 'Imported Fitting Settings from: %s'%fname
                self.statusBar().showMessage('Imported Fitting Settings to: %s'%fname)


            except ValueError:
                print "Error in loading JSON file: %s."%(fname)
                print "Verify that the configuration file is properly formatted."

            except KeyError:
                import_type = 'fitting settings'
                print 'Error in importing %s from: %s.'%(import_type, fname)
                print 'Verify that this settings file is the right kind for this import.'


    def export_to_carboninp(self):
        """
        Exports all current settings to a new CARBON.INP file
        This method is the part where user selects the destination.

        :return:
        """

        if self.default_carboninp_export_dir:

            fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export CARBON.INP',
                                                              self.default_carboninp_export_dir, filter="*.inp")
        else:
            fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export CARBON.INP',
                                                          os.path.join(user_data_directory, 'config', 'fitting settings'), filter="*.inp")

        if fname:
            self.write_carboninp(fname)
            self.default_carboninp_export_dir, _ = os.path.split(fname)

            print 'Exported in CARBON.INP format to: %s'%fname
            self.statusBar().showMessage('Exported in CARBON.INP format to: %s'%fname)

    def write_carboninp(self, destination, disable_fit = False):
        """
        Method which writes the currently loaded data to a Carbon.inp file

        :param destination: - File path to export to
        :param disable_fit: - Boolean which disables fit and only performs a pattern calculation if true

        :return:
        """


        export_file = open(destination, 'w')

        export_file.write("SCAN.DAT\n")

        #
        export_file.write("  %5.2f    %5.2f %6.6f       %d  "%(self.theta_min_value.value(),
                                                        self.theta_max_value.value(),
                                                        self.wavelength.value(),
                                                        self.nskip.value())+
                          "            Thmin   Thmax   Lambda  Nskip\n")

        if self.number_layers.currentIndex() == 0:
            num_layers = 1
        else:
            num_layers = 2
        export_file.write("     18        %d        %d       %d  "%(self.n_phi.value(),
                                                                   self.n_sg.value(),
                                                                   num_layers
                                                                   )
                           +"            Npar    Nphi    Nsg     Nlayer\n")

        export_file.write(" %6.3f   %6.3f   %6.3f  %6.3f   %6.3f"%(self.sample_density.value(),
                                                                                 self.goniometer_radius.value(),
                                                                                 self.sample_depth.value(),
                                                                                 self.sample_width.value(),
                                                                                 self.beam_width.value()

                                                                                 )
                          +"     Rdens   L0      Wd      Ww      Bw\n")


        if not disable_fit:
            iterations = self.iterations.value()
        else:
            iterations = 0

        export_file.write("      %d   %6.5f                        "%(iterations, self.epsilon.value())+
                          "       Itmax   Eps\n")

        enable_gc = 0

        export_file.write("      %d   %6.5f                        "%(enable_gc, 0.0)+
                          "       Itest   Dx\n")

        for index, label in enumerate(self.parameter_labels):

            param_value = self.parameter_list[index].value()
            param_str = ("%5.4E"%param_value).rjust(12)
            if self.parameter_enable_list[index].isChecked():
                param_str += "  1    "
            else:
                param_str += "  0    "

            param_str += label.text().ljust(70)
            param_str += "\n"

            export_file.write(param_str)


    def import_from_carboninp(self):

        """
        Method to read all settings from a carbon.inp file
        This is the method which the user choses the file

        :return:
        """

        if self.default_carboninp_import_dir:
            fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.default_carboninp_import_dir, filter="*.inp")
        else:
            fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', user_data_directory, filter="*.inp")

        if fname:
            self.read_carboninp(fname)
            self.default_carboninp_import_dir, _ = os.path.split(fname)

            print 'Imported CARBON.INP parameters from: %s' % fname
            self.statusBar().showMessage('Imported CARBON.INP parameters from: %s' % fname)

    def read_carboninp(self, filename):
        """
        Method which processes loading of data from carbon.inp file

        :param filename: file path to load data from
        :return:
        """


        config_file = open(filename, 'r')

        data_lines = config_file.readlines()

        # Thetamin, theta max, wavelength, nskip
        data_elements_1 = data_lines[1].split()

        self.theta_min_value.setValue(float(data_elements_1[0]))
        self.theta_max_value.setValue(float(data_elements_1[1]))
        self.wavelength.setValue(float(data_elements_1[2]))
        self.nskip.setValue(int(data_elements_1[3]))

        data_elements_2 = data_lines[2].split()

        self.n_phi.setValue(float(data_elements_2[1]))
        self.n_sg.setValue(float(data_elements_2[2]))


        if int(data_elements_2[3]) == 1:
            self.number_layers.setCurrentIndex(0)
        elif int(data_elements_2[3]) == 2:
            self.number_layers.setCurrentIndex(1)
        else:
            print "Number of layers is not 1 or 2. Setting to 1"
            self.number_layers.setCurrentIndex(0)

        # Diffractometer Parameters
        data_elements_3 = data_lines[3].split()
        self.sample_density.setValue(float(data_elements_3[0]))
        self.goniometer_radius.setValue(float(data_elements_3[1]))
        self.sample_depth.setValue(float(data_elements_3[2]))
        self.sample_width.setValue(float(data_elements_3[3]))
        self.beam_width.setValue(float(data_elements_3[4]))


        data_elements_4 = data_lines[4].split()

        self.iterations.setValue(int(data_elements_4[0]))
        self.epsilon.setValue(float(data_elements_4[1]))

        data_elements_5 = data_lines[5].split()

        for index, line in enumerate(data_lines[6:]):
            config_elements = line.split()

            if "*" in config_elements[0]:
                print "Warning: Bad parameter found in "+self.parameter_labels[index].text()
                print "Setting parameter value to 0"
                param_value = 0
            else:

                param_value = float(config_elements[0])

            if config_elements[1] == '1':
                param_enable = True
            else:
                param_enable = False

            self.parameter_list[index].setValue(param_value)
            self.parameter_enable_list[index].setChecked(param_enable)

        errors, warnings = self.check_fitting_parameters()
        if errors+warnings > 0:
            print "Found %d errors and %d warnings. Please ensure parameters are physically meaningful."%(errors, warnings)

    def write_scan_data(self, output_file):
        """
        Uses currently loaded XRD pattern data and writes it to a format that carbonxs.exe can read

        :param output_file: file path for the destination
        :return:
        """


        scan_file = open(output_file, 'w')

        for x, y in zip(*(self.x_data, self.y_data)):

            data_line = "%4.2f\t%4.2f\n"%(x, y)

            scan_file.write(data_line)

    def pre_run_sanity_check(self, fit_mode):
        """
        Performs sanity checks on current settings and parameters before a fit is run.

        :return:
        """

        errors = 0

        if self.iterations.value() < 1 and fit_mode:
            print "Number of iterations is less than 1. No fitting will be performed."
            print "Use Fitting -> Calculate Pattern to perform pattern calculation."
            errors += 1

        if not any([enable.isChecked() for enable in self.parameter_enable_list]) and fit_mode:
            print "Error: No fitting parameters are enabled."
            errors +=1


        if self.sample_density.value() > 1.0 or self.sample_density.value() < 0.0:
            print "Sample Density must be between 0 and 1"
            errors += 1


        fit_errors, warnings = self.check_fitting_parameters()

        errors += fit_errors

        if errors > 0:
            print "Found %d errors and %d warnings. Aborting."%(errors, warnings)
            return False
        else:
            print "Parameter check passed with 0 errors and %d warnings. Proceeding with fit."%warnings
            return True


    def check_fitting_parameters(self):
        """
        Performs sanity check and alerts the user if values may potentially be out of bounds

        :return:
        """

        print "Performing checks on fitting parameters."

        errors = 0
        warnings = 0

        if not any([fit_parameter.value() for fit_parameter in self.parameter_list]):
            print "ERROR: No non-zero fitting parameters have been set. Please input an initial set of parameters"
            errors += 1


        if not any([self.fit_settings[key].value() for key in self.fit_settings.keys() if key != 'number_layers']):
            print "ERROR: No non-zero fit settings have been set. Please input a set of fit settings."
            errors += 1

        if not any([diff_setting.value() for diff_setting in self.diff_settings]):
            print "ERROR: No non-zero diffractometer settings have been set. Please input a set of diffractometer settings."
            errors += 1

        if self.param_07.value() < 0:
            print "ERROR: A (In place cell constant) must be greater than 0."
            errors += 1
        if self.param_08.value() < 0:
            print "ERROR: d002 (Interlayer Spacing) must be greater than 0."
            errors += 1
        if self.param_09.value() < 0:
            print "ERROR: La (Coherence Length) must be greater than 0."
            errors += 1
        if self.param_10.value() < 0:
            print "ERROR: M (Number of Layers) must be greater than 0."
            errors += 1

        if self.param_12.value() < 0:
            print "ERROR: Dab (In plane strain) must be greater than 0."
            errors += 1
        if self.param_13.value() < 0:
            print "ERROR: Del (Interplanar strain) must be greater than 0."
            errors += 1
        if self.param_14.value() > 1 or  self.param_14.value() < 0:
            print "ERROR: Pr must be between 0 and 1."
            errors += 1
        if self.param_15.value() > 1 or  self.param_15.value() < 0:
            print "ERROR: g (1 layer model) or Pt (2 layer model) must be between 0 and 1."
            errors += 1
        if self.param_16.value() < 0:
            print "Warning: Debye Waller Temperature factor is less than 0."
            warnings += 1
        if self.param_17.value() < 0:
            print "Warning: Preferential Orientation Factor is less than 0."
            warnings += 1

        return errors, warnings

    def start_fitting_process(self):
        """
        Calls the fitting process to begin
        :return:
        """


        # Verifies that XRD pattern data has been loaded
        if len(self.x_data) > 0 and len(self.y_data) > 0:
            print "Beginning fitting process."

            # If all sanity checks pass, proceed with fit
            if self.pre_run_sanity_check(True):
                self.call_fit_program()

        # If not, prompt the user to load data
        else:

            reply = QtGui.QMessageBox.question(self, 'No XRD Pattern Loaded',
                                               "Do you want to load a pattern?", QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:

                self.open_pattern()
                # If a pattern has been loaded, proceeed with fit.
                if len(self.x_data) > 0 and len(self.y_data) > 0 and self.pre_run_sanity_check(True):
                    print "Loaded an XRD pattern"
                    self.call_fit_program()

    def call_fit_program(self):
        """
        Starts the carbonxs.exe fit process
        :return:
        """

        os.chdir(os.path.join(base_directory, 'carbonxs'))

        print "Writing carbon.inp to the carbonxs directory."

        self.write_carboninp("carbon.inp")

        print "Writing SCAN.DAT to the carbonxs directory."

        self.write_scan_data("SCAN.DAT")
        self.pattern_calc_flag = False
        self.append_to_buffer = True

        print "Calling CarbonXS."

        if "win32" in sys.platform:
            print "Windows detected - calling carbonxs_gfortran.exe"
            self.fitting_process.start('carbonxs_gfortran.exe')
        elif 'linux' in sys.platform or 'darwin' in sys.platform:
            print "Linux/OSX detected - calling carbonxs_app"
            self.fitting_process.start('./carbonxs_app')
        else:
            print "WARNING UNSUPPORTED PLATFORM"

        # Sets menu flags to disable start of another process and enable aborting fit process
        self.menu_start_fit.setEnabled(False)
        self.menu_calculate_pattern.setEnabled(False)
        self.calculate_pattern_button.setEnabled(False)
        self.fit_pattern_button.setEnabled(False)
        self.menu_abort_fit.setEnabled(True)
        self.abort_fit_button.setEnabled(True)
        self.back_button.setEnabled(False)
        self.forward_button.setEnabled(False)
        os.chdir('..')


    def calculate_pattern(self, append_to_buffer=True):
        """
        Calculate a pattern based on the currently loaded parameters without performing a fit
        :return:
        """

        if self.pre_run_sanity_check(False):
            self.append_to_buffer = append_to_buffer
            print "Beginning pattern calculation process."
            os.chdir(os.path.join(base_directory, 'carbonxs'))
            print "Wrote carbon.inp to the carbonxs directory."
            self.write_carboninp("carbon.inp", disable_fit=True)
            print "Calling CarbonXS."
            self.pattern_calc_flag = True
            self.menu_start_fit.setEnabled(False)
            self.menu_calculate_pattern.setEnabled(False)
            self.calculate_pattern_button.setEnabled(False)
            self.fit_pattern_button.setEnabled(False)

            if "win32" in sys.platform:
                print "Windows detected - calling carbonxs_gfortran.exe"
                self.fitting_process.start('carbonxs_gfortran.exe')
            elif 'linux' in sys.platform or 'darwin' in sys.platform:
                print "Linux/OSX detected - calling carbonxs_app"
                self.fitting_process.start('./carbonxs_app')
            else:
                print "WARNING UNSUPPORTED PLATFORM"

            self.menu_abort_fit.setEnabled(True)
            self.abort_fit_button.setEnabled(True)

            os.chdir('..')

    def abort_fit_process(self):
        """
        Kills the currently running carbon.exe process
        :return:
        """

        self.fitting_process.kill()
        self.menu_abort_fit.setEnabled(False)
        self.abort_fit_button.setEnabled(False)

        self.menu_start_fit.setEnabled(True)
        self.menu_calculate_pattern.setEnabled(True)
        self.calculate_pattern_button.setEnabled(True)
        self.fit_pattern_button.setEnabled(True)
        self.abort_flag = True
        self.check_undo_index()

    def fitting_finished(self, append_to_buffer):
        """
        Method to handle completion of fitting process
        :return:
        """

        if not self.abort_flag:

            print "CarbonXS Process Complete"

            # Exit Code 0 indicates successful completion
            if self.fitting_process.exitCode() == 0:

                if not self.pattern_calc_flag:
                    print "Reading new carbon.inp data and plotting new data"
                    self.read_carboninp(os.path.join(base_directory, 'carbonxs', 'carbon.inp'))



                self.plot_fit_results()

                # If in fitting mode, give option to export fitting results
                if not self.pattern_calc_flag:

                    reply = QtGui.QMessageBox.question(self, 'Fit Completed',
                                                       "Export the results?", QtGui.QMessageBox.Yes |
                                                       QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.export_fit_results()

                if self.append_to_buffer:
                    # Truncate buffer at current index

                    if self.undo_index < len(self.undo_buffer) - 1 and self.undo_buffer:
                        self.undo_buffer = self.undo_buffer[:self.undo_index+1]


                    self.undo_buffer.append(FittingParams(self.parameter_list, self.parameter_enable_list,
                                                          self.fit_settings, self.diff_settings))
                    self.undo_index = len(self.undo_buffer)-1

                    self.check_undo_index()

            # Exit Code 1 indicates a crash in CarbonXS
            # Do NOT load any settings the program wrote
            elif self.fitting_process.exitCode() == 1:
                print "Error: Fit failed due to crash in CarbonXS"
            else:
                print "Other error occurred"

            # Re-enable buttons to start process and disable buttons that abort process
            self.menu_abort_fit.setEnabled(False)
            self.abort_fit_button.setEnabled(False)

            self.menu_start_fit.setEnabled(True)
            self.menu_calculate_pattern.setEnabled(True)
            self.calculate_pattern_button.setEnabled(True)
            self.fit_pattern_button.setEnabled(True)


        else:
            print "\n\n Fitting process aborted"

            self.abort_flag = False


    def export_fit_results(self):
        """
        Copies the carbon.out, carbon.dat, and CARBON.INP files currently in the carbonxs
        directory to a destination of your choice.
        :return:
        """

        if not len(self.x_data):
            reply = QtGui.QMessageBox.warning(self, 'Export Data',
                    "No data currently loaded.",
                                              QtGui.QMessageBox.Close)

            return

        if self.default_export_dir:

             fname, _ = QtGui.QFileDialog.getSaveFileName(self, 'Select Base Name For Results',self.default_export_dir,
                                                     "Full Export (*);; Jade MDI Format (*.mdi)")
        else:
             fname, _ = QtGui.QFileDialog.getSaveFileName(self, 'Select Base Name For Results',user_data_directory,
                                                     "Full Export (*);; Jade MDI Format (*.mdi)")


        if fname:

            if fname.endswith('.mdi'):
                print "Exporting fit results to Jade MDI Format"

                directory, _ = os.path.split(fname)

                data_io.write_mdi_file(fname, self.x_fit_data, self.y_fit_data, wavelength=self.wavelength.value())
                self.default_export_dir = directory

            else:
                for data_file, export_suffix in [('carbon.out', '_carbon_out.txt'), ('carbon.dat', '_carbon_dat.txt'), ('CARBON.INP','_CARBON.INP')]:

                    # Checks if the files exist in the directory
                    if data_file in os.listdir('carbonxs'):

                        destination = fname + export_suffix
                        directory, filename = os.path.split(destination)

                        # Checks if the destination files already exists
                        if os.path.exists(destination):

                            # Prompts user to overwrite if it does
                            reply = QtGui.QMessageBox.question(self, 'Fit Completed',
                                                               "%s exists. Overwrite?"%filename, QtGui.QMessageBox.Yes |
                                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                            if reply == QtGui.QMessageBox.Yes:

                                self.default_export_dir = directory
                                shutil.copy(os.path.join(base_directory, 'carbonxs', data_file), fname + export_suffix)
                                print "Copied %s file to %s. (Overwrote old file)" % (data_file, destination)
                            else:
                                print "%s already exists. Did not overwrite." % destination

                        else:

                            self.default_export_dir =directory

                            shutil.copy(os.path.join(base_directory, 'carbonxs', data_file), destination)
                            print "Copied %s file to %s" %(data_file, destination)




    def go_back(self):
        """
        Go to the previous item in the data buffer and plot the result
        
        :return: 
        """

        if self.undo_index - 1 >= 0:

            load_params = self.undo_buffer[self.undo_index-1]
            self.update_from_buffer(load_params)

            self.undo_index -= 1

            self.calculate_pattern(append_to_buffer=False)
            self.check_undo_index()
        else:
            print "Cannot go further back"

    def go_forward(self):
        """
        Go to the next item in the data buffer and plot the result
        
        :return: 
        """

        if self.undo_index + 1 < len(self.undo_buffer):

            load_params = self.undo_buffer[self.undo_index+1]
            self.update_from_buffer(load_params)

            self.undo_index += 1
            self.calculate_pattern(append_to_buffer=False)
            self.check_undo_index()
        else:
            print "Cannot go further forward"

    def update_from_buffer(self, load_params):
        """
        Update the fit parameters, fit settings, and diffractometer_settings from a buffer element
        :param load_params:
        :return:
        """

        for index, value in enumerate(load_params.param_values):
            self.parameter_list[index].setValue(value)
        for en_index, enabled in enumerate(load_params.param_flags):
            self.parameter_enable_list[en_index].setChecked(enabled)

        for key in load_params.fit_settings.keys():

            if key == 'number_layers':
                self.fit_settings[key].setCurrentIndex(load_params.fit_settings[key])
            else:
                self.fit_settings[key].setValue(load_params.fit_settings[key])

        for ds_index, ds_value in enumerate(load_params.diff_values):
            self.diff_settings[ds_index].setValue(ds_value)



    def check_undo_index(self):
        """
        Checks whether the undo index is at the beginning or end of its limits and disable the buttons respectively
        :return: 
        
        """

        if self.undo_index == 0:
            self.back_button.setEnabled(False)
        else:
            self.back_button.setEnabled(True)

        if self.undo_index == len(self.undo_buffer)-1 or not self.undo_buffer:
            self.forward_button.setEnabled(False)
        else:
            self.forward_button.setEnabled(True)


    # Help Menu Methods
    def open_documentation(self):

        """
        Opens the documentation in /docs/index.html
        :return:
        """
        webbrowser.open("https://lktsui.github.io/carbon_xs_gui/")


    def open_bug_report_page(self):
        """
        Opens the a link to the bug report page
        :return:
        """
        webbrowser.open("https://github.com/lktsui/carbon_xs_gui/issues")

    def open_about_dialog(self):
        """
        Opens the a link to the bug report page
        :return:
        """

        reply = QtGui.QMessageBox.information(self, 'About',
        "Version %s.\nGUI by Lok-kun Tsui.\nCarbonXS by H. Shi, J.N. Reimers, and J.R. Dahn."%self.version,
                                              QtGui.QMessageBox.Close)
    #

    def closeEvent(self, event):
        print "Closing program"
        self.write_config()


def main():

    version = "1.3.1"

    app = QtGui.QApplication(sys.argv)


    ex = MainWindow(version)

    console_stream = ConsoleStream()
    console_stream.message.connect(ex.on_stream_message)

    sys.stdout = console_stream
    sys.stderr = console_stream

    ex.data_init()

    sys.exit(app.exec_())




if __name__ == '__main__':

    # Check if carbon program is present
    print "Checking if programs are available"

    if  'darwin' in sys.platform or 'linux' in sys.platform:
        if 'carbonxs_app' not in os.listdir(os.path.join(base_directory, 'carbonxs')):
            print "ERROR: carbonxs_app is not present in the carbonxs directory"
            print "This indicates that a version of the carbonxs program has not yet been compiled"
            print "Please compile (see compiling.txt) the Fortran program using GCC."
            print "Alternately, run compile.sh"
            sys.exit()
        else:
            print "Found CarbonXS!"


    elif 'win32' in sys.platform:
        if 'carbonxs_gfortran.exe' not in os.listdir(os.path.join(base_directory, 'carbonxs')):
            print "ERROR! carbonxs_gfortran.exe is not in the carbonxs directory"
            print "Please make sure this program has been correctly extracted."
            sys.exit()
        else:
            print "Found CarbonXS!"
    main()
