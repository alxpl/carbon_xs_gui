# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\untitled\main_window_scalable.ui'
#
# Created: Tue Apr 18 11:37:55 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 858)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.left_side = QtGui.QVBoxLayout()
        self.left_side.setObjectName("left_side")
        self.label_fitting_params = QtGui.QLabel(self.centralwidget)
        self.label_fitting_params.setMinimumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_fitting_params.setFont(font)
        self.label_fitting_params.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fitting_params.setObjectName("label_fitting_params")
        self.left_side.addWidget(self.label_fitting_params)
        self.parameter_select_buttons = QtGui.QHBoxLayout()
        self.parameter_select_buttons.setObjectName("parameter_select_buttons")
        self.enable_all_button = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enable_all_button.sizePolicy().hasHeightForWidth())
        self.enable_all_button.setSizePolicy(sizePolicy)
        self.enable_all_button.setObjectName("enable_all_button")
        self.parameter_select_buttons.addWidget(self.enable_all_button)
        self.enable_none_button = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enable_none_button.sizePolicy().hasHeightForWidth())
        self.enable_none_button.setSizePolicy(sizePolicy)
        self.enable_none_button.setObjectName("enable_none_button")
        self.parameter_select_buttons.addWidget(self.enable_none_button)
        self.enable_invert_button = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enable_invert_button.sizePolicy().hasHeightForWidth())
        self.enable_invert_button.setSizePolicy(sizePolicy)
        self.enable_invert_button.setObjectName("enable_invert_button")
        self.parameter_select_buttons.addWidget(self.enable_invert_button)
        self.left_side.addLayout(self.parameter_select_buttons)
        self.fitting_parameters_list = QtGui.QGridLayout()
        self.fitting_parameters_list.setObjectName("fitting_parameters_list")
        self.param_09 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_09.setObjectName("param_09")
        self.fitting_parameters_list.addWidget(self.param_09, 12, 0, 1, 1)
        self.param_10 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_10.setObjectName("param_10")
        self.fitting_parameters_list.addWidget(self.param_10, 13, 0, 1, 1)
        self.param_16 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_16.setObjectName("param_16")
        self.fitting_parameters_list.addWidget(self.param_16, 19, 0, 1, 1)
        self.param_11 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_11.setObjectName("param_11")
        self.fitting_parameters_list.addWidget(self.param_11, 14, 0, 1, 1)
        self.param_12 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_12.setObjectName("param_12")
        self.fitting_parameters_list.addWidget(self.param_12, 15, 0, 1, 1)
        self.param_enable_02 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_02.setObjectName("param_enable_02")
        self.fitting_parameters_list.addWidget(self.param_enable_02, 5, 2, 1, 1)
        self.param_enable_03 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_03.setObjectName("param_enable_03")
        self.fitting_parameters_list.addWidget(self.param_enable_03, 6, 2, 1, 1)
        self.param_05 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_05.setObjectName("param_05")
        self.fitting_parameters_list.addWidget(self.param_05, 8, 0, 1, 1)
        self.param_06 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_06.setObjectName("param_06")
        self.fitting_parameters_list.addWidget(self.param_06, 9, 0, 1, 1)
        self.param_08 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_08.setObjectName("param_08")
        self.fitting_parameters_list.addWidget(self.param_08, 11, 0, 1, 1)
        self.param_enable_12 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_12.setObjectName("param_enable_12")
        self.fitting_parameters_list.addWidget(self.param_enable_12, 15, 2, 1, 1)
        self.param_label_15 = QtGui.QLabel(self.centralwidget)
        self.param_label_15.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_15.setFont(font)
        self.param_label_15.setObjectName("param_label_15")
        self.fitting_parameters_list.addWidget(self.param_label_15, 18, 4, 1, 1)
        self.param_label_17 = QtGui.QLabel(self.centralwidget)
        self.param_label_17.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_17.setFont(font)
        self.param_label_17.setObjectName("param_label_17")
        self.fitting_parameters_list.addWidget(self.param_label_17, 20, 4, 1, 1)
        self.param_label_14 = QtGui.QLabel(self.centralwidget)
        self.param_label_14.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_14.setFont(font)
        self.param_label_14.setObjectName("param_label_14")
        self.fitting_parameters_list.addWidget(self.param_label_14, 17, 4, 1, 1)
        self.param_label_11 = QtGui.QLabel(self.centralwidget)
        self.param_label_11.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_11.setFont(font)
        self.param_label_11.setObjectName("param_label_11")
        self.fitting_parameters_list.addWidget(self.param_label_11, 14, 4, 1, 1)
        self.param_label_09 = QtGui.QLabel(self.centralwidget)
        self.param_label_09.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_09.setFont(font)
        self.param_label_09.setObjectName("param_label_09")
        self.fitting_parameters_list.addWidget(self.param_label_09, 12, 4, 1, 1)
        self.param_label_03 = QtGui.QLabel(self.centralwidget)
        self.param_label_03.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_03.setFont(font)
        self.param_label_03.setObjectName("param_label_03")
        self.fitting_parameters_list.addWidget(self.param_label_03, 6, 4, 1, 1)
        self.param_label_10 = QtGui.QLabel(self.centralwidget)
        self.param_label_10.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_10.setFont(font)
        self.param_label_10.setObjectName("param_label_10")
        self.fitting_parameters_list.addWidget(self.param_label_10, 13, 4, 1, 1)
        self.param_label_02 = QtGui.QLabel(self.centralwidget)
        self.param_label_02.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_02.setFont(font)
        self.param_label_02.setObjectName("param_label_02")
        self.fitting_parameters_list.addWidget(self.param_label_02, 5, 4, 1, 1)
        self.param_label_01 = QtGui.QLabel(self.centralwidget)
        self.param_label_01.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_01.setFont(font)
        self.param_label_01.setObjectName("param_label_01")
        self.fitting_parameters_list.addWidget(self.param_label_01, 4, 4, 1, 1)
        self.param_enable_09 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_09.setObjectName("param_enable_09")
        self.fitting_parameters_list.addWidget(self.param_enable_09, 12, 2, 1, 1)
        self.param_enable_10 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_10.setObjectName("param_enable_10")
        self.fitting_parameters_list.addWidget(self.param_enable_10, 13, 2, 1, 1)
        self.param_enable_14 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_14.setObjectName("param_enable_14")
        self.fitting_parameters_list.addWidget(self.param_enable_14, 17, 2, 1, 1)
        self.param_enable_01 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_01.setObjectName("param_enable_01")
        self.fitting_parameters_list.addWidget(self.param_enable_01, 4, 2, 1, 1)
        self.param_enable_13 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_13.setObjectName("param_enable_13")
        self.fitting_parameters_list.addWidget(self.param_enable_13, 16, 2, 1, 1)
        self.param_enable_15 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_15.setObjectName("param_enable_15")
        self.fitting_parameters_list.addWidget(self.param_enable_15, 18, 2, 1, 1)
        self.param_00 = QtGui.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.param_00.sizePolicy().hasHeightForWidth())
        self.param_00.setSizePolicy(sizePolicy)
        self.param_00.setObjectName("param_00")
        self.fitting_parameters_list.addWidget(self.param_00, 3, 0, 1, 1)
        self.param_enable_17 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_17.setObjectName("param_enable_17")
        self.fitting_parameters_list.addWidget(self.param_enable_17, 20, 2, 1, 1)
        self.param_07 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_07.setObjectName("param_07")
        self.fitting_parameters_list.addWidget(self.param_07, 10, 0, 1, 1)
        self.param_13 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_13.setObjectName("param_13")
        self.fitting_parameters_list.addWidget(self.param_13, 16, 0, 1, 1)
        self.param_14 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_14.setObjectName("param_14")
        self.fitting_parameters_list.addWidget(self.param_14, 17, 0, 1, 1)
        self.param_17 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_17.setObjectName("param_17")
        self.fitting_parameters_list.addWidget(self.param_17, 20, 0, 1, 1)
        self.param_15 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_15.setObjectName("param_15")
        self.fitting_parameters_list.addWidget(self.param_15, 18, 0, 1, 1)
        self.param_label_06 = QtGui.QLabel(self.centralwidget)
        self.param_label_06.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_06.setFont(font)
        self.param_label_06.setObjectName("param_label_06")
        self.fitting_parameters_list.addWidget(self.param_label_06, 9, 4, 1, 1)
        self.param_label_05 = QtGui.QLabel(self.centralwidget)
        self.param_label_05.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_05.setFont(font)
        self.param_label_05.setObjectName("param_label_05")
        self.fitting_parameters_list.addWidget(self.param_label_05, 8, 4, 1, 1)
        self.param_label_04 = QtGui.QLabel(self.centralwidget)
        self.param_label_04.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_04.setFont(font)
        self.param_label_04.setObjectName("param_label_04")
        self.fitting_parameters_list.addWidget(self.param_label_04, 7, 4, 1, 1)
        self.param_label_08 = QtGui.QLabel(self.centralwidget)
        self.param_label_08.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_08.setFont(font)
        self.param_label_08.setObjectName("param_label_08")
        self.fitting_parameters_list.addWidget(self.param_label_08, 11, 4, 1, 1)
        self.param_label_12 = QtGui.QLabel(self.centralwidget)
        self.param_label_12.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_12.setFont(font)
        self.param_label_12.setObjectName("param_label_12")
        self.fitting_parameters_list.addWidget(self.param_label_12, 15, 4, 1, 1)
        self.param_label_07 = QtGui.QLabel(self.centralwidget)
        self.param_label_07.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_07.setFont(font)
        self.param_label_07.setObjectName("param_label_07")
        self.fitting_parameters_list.addWidget(self.param_label_07, 10, 4, 1, 1)
        self.param_label_16 = QtGui.QLabel(self.centralwidget)
        self.param_label_16.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_16.setFont(font)
        self.param_label_16.setObjectName("param_label_16")
        self.fitting_parameters_list.addWidget(self.param_label_16, 19, 4, 1, 1)
        self.param_label_13 = QtGui.QLabel(self.centralwidget)
        self.param_label_13.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_13.setFont(font)
        self.param_label_13.setObjectName("param_label_13")
        self.fitting_parameters_list.addWidget(self.param_label_13, 16, 4, 1, 1)
        self.param_label_00 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.param_label_00.sizePolicy().hasHeightForWidth())
        self.param_label_00.setSizePolicy(sizePolicy)
        self.param_label_00.setMinimumSize(QtCore.QSize(0, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_00.setFont(font)
        self.param_label_00.setObjectName("param_label_00")
        self.fitting_parameters_list.addWidget(self.param_label_00, 3, 4, 1, 1)
        self.param_02 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_02.setObjectName("param_02")
        self.fitting_parameters_list.addWidget(self.param_02, 5, 0, 1, 1)
        self.param_03 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_03.setObjectName("param_03")
        self.fitting_parameters_list.addWidget(self.param_03, 6, 0, 1, 1)
        self.param_04 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_04.setObjectName("param_04")
        self.fitting_parameters_list.addWidget(self.param_04, 7, 0, 1, 1)
        self.param_enable_08 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_08.setObjectName("param_enable_08")
        self.fitting_parameters_list.addWidget(self.param_enable_08, 11, 2, 1, 1)
        self.param_enable_00 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_00.setObjectName("param_enable_00")
        self.fitting_parameters_list.addWidget(self.param_enable_00, 3, 2, 1, 1)
        self.param_enable_16 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_16.setObjectName("param_enable_16")
        self.fitting_parameters_list.addWidget(self.param_enable_16, 19, 2, 1, 1)
        self.param_01 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.param_01.setObjectName("param_01")
        self.fitting_parameters_list.addWidget(self.param_01, 4, 0, 1, 1)
        self.param_enable_11 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_11.setObjectName("param_enable_11")
        self.fitting_parameters_list.addWidget(self.param_enable_11, 14, 2, 1, 1)
        self.param_enable_04 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_04.setObjectName("param_enable_04")
        self.fitting_parameters_list.addWidget(self.param_enable_04, 7, 2, 1, 1)
        self.param_enable_06 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_06.setObjectName("param_enable_06")
        self.fitting_parameters_list.addWidget(self.param_enable_06, 9, 2, 1, 1)
        self.param_enable_07 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_07.setObjectName("param_enable_07")
        self.fitting_parameters_list.addWidget(self.param_enable_07, 10, 2, 1, 1)
        self.param_enable_05 = QtGui.QCheckBox(self.centralwidget)
        self.param_enable_05.setObjectName("param_enable_05")
        self.fitting_parameters_list.addWidget(self.param_enable_05, 8, 2, 1, 1)
        self.left_side.addLayout(self.fitting_parameters_list)
        self.label_fitting_settings = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_fitting_settings.sizePolicy().hasHeightForWidth())
        self.label_fitting_settings.setSizePolicy(sizePolicy)
        self.label_fitting_settings.setMinimumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setWeight(50)
        font.setBold(False)
        self.label_fitting_settings.setFont(font)
        self.label_fitting_settings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fitting_settings.setObjectName("label_fitting_settings")
        self.left_side.addWidget(self.label_fitting_settings)
        self.fitting_settings_list = QtGui.QGridLayout()
        self.fitting_settings_list.setObjectName("fitting_settings_list")
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.fitting_settings_list.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.fitting_settings_list.addWidget(self.label_8, 2, 3, 1, 1)
        self.epsilon = QtGui.QDoubleSpinBox(self.centralwidget)
        self.epsilon.setObjectName("epsilon")
        self.fitting_settings_list.addWidget(self.epsilon, 1, 3, 1, 1)
        self.theta_min_value = QtGui.QDoubleSpinBox(self.centralwidget)
        self.theta_min_value.setObjectName("theta_min_value")
        self.fitting_settings_list.addWidget(self.theta_min_value, 1, 0, 1, 1)
        self.iterations = QtGui.QSpinBox(self.centralwidget)
        self.iterations.setObjectName("iterations")
        self.fitting_settings_list.addWidget(self.iterations, 1, 2, 1, 1)
        self.theta_min_label = QtGui.QLabel(self.centralwidget)
        self.theta_min_label.setObjectName("theta_min_label")
        self.fitting_settings_list.addWidget(self.theta_min_label, 0, 0, 1, 1)
        self.theta_max_label = QtGui.QLabel(self.centralwidget)
        self.theta_max_label.setObjectName("theta_max_label")
        self.fitting_settings_list.addWidget(self.theta_max_label, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.fitting_settings_list.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.fitting_settings_list.addWidget(self.label_6, 2, 1, 1, 1)
        self.number_layers = QtGui.QComboBox(self.centralwidget)
        self.number_layers.setObjectName("number_layers")
        self.number_layers.addItem("")
        self.number_layers.addItem("")
        self.fitting_settings_list.addWidget(self.number_layers, 3, 1, 1, 1)
        self.nskip = QtGui.QSpinBox(self.centralwidget)
        self.nskip.setObjectName("nskip")
        self.fitting_settings_list.addWidget(self.nskip, 3, 0, 1, 1)
        self.n_sg = QtGui.QSpinBox(self.centralwidget)
        self.n_sg.setObjectName("n_sg")
        self.fitting_settings_list.addWidget(self.n_sg, 3, 3, 1, 1)
        self.gradient_check_enable = QtGui.QComboBox(self.centralwidget)
        self.gradient_check_enable.setObjectName("gradient_check_enable")
        self.gradient_check_enable.addItem("")
        self.gradient_check_enable.addItem("")
        self.fitting_settings_list.addWidget(self.gradient_check_enable, 5, 1, 1, 1)
        self.theta_max_value = QtGui.QDoubleSpinBox(self.centralwidget)
        self.theta_max_value.setObjectName("theta_max_value")
        self.fitting_settings_list.addWidget(self.theta_max_value, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.fitting_settings_list.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.fitting_settings_list.addWidget(self.label_7, 2, 2, 1, 1)
        self.n_phi = QtGui.QSpinBox(self.centralwidget)
        self.n_phi.setObjectName("n_phi")
        self.fitting_settings_list.addWidget(self.n_phi, 3, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.fitting_settings_list.addWidget(self.label_9, 4, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.fitting_settings_list.addWidget(self.label_10, 4, 2, 1, 1)
        self.gradient_check_delta = QtGui.QDoubleSpinBox(self.centralwidget)
        self.gradient_check_delta.setObjectName("gradient_check_delta")
        self.fitting_settings_list.addWidget(self.gradient_check_delta, 5, 2, 1, 1)
        self.left_side.addLayout(self.fitting_settings_list)
        self.label_diffractometer_settings = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_diffractometer_settings.setFont(font)
        self.label_diffractometer_settings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_diffractometer_settings.setObjectName("label_diffractometer_settings")
        self.left_side.addWidget(self.label_diffractometer_settings)
        self.diffractometer_settings_list = QtGui.QGridLayout()
        self.diffractometer_settings_list.setObjectName("diffractometer_settings_list")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.diffractometer_settings_list.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setObjectName("label_14")
        self.diffractometer_settings_list.addWidget(self.label_14, 2, 2, 1, 1)
        self.sample_depth = QtGui.QDoubleSpinBox(self.centralwidget)
        self.sample_depth.setObjectName("sample_depth")
        self.diffractometer_settings_list.addWidget(self.sample_depth, 1, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.diffractometer_settings_list.addWidget(self.label_11, 0, 2, 1, 1)
        self.wavelength = QtGui.QDoubleSpinBox(self.centralwidget)
        self.wavelength.setObjectName("wavelength")
        self.diffractometer_settings_list.addWidget(self.wavelength, 1, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.diffractometer_settings_list.addWidget(self.label_13, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.diffractometer_settings_list.addWidget(self.label, 0, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.diffractometer_settings_list.addWidget(self.label_12, 2, 0, 1, 1)
        self.sample_width = QtGui.QDoubleSpinBox(self.centralwidget)
        self.sample_width.setObjectName("sample_width")
        self.diffractometer_settings_list.addWidget(self.sample_width, 1, 2, 1, 1)
        self.goniometer_radius = QtGui.QDoubleSpinBox(self.centralwidget)
        self.goniometer_radius.setObjectName("goniometer_radius")
        self.diffractometer_settings_list.addWidget(self.goniometer_radius, 3, 0, 1, 1)
        self.beam_width = QtGui.QDoubleSpinBox(self.centralwidget)
        self.beam_width.setObjectName("beam_width")
        self.diffractometer_settings_list.addWidget(self.beam_width, 3, 1, 1, 1)
        self.sample_density = QtGui.QDoubleSpinBox(self.centralwidget)
        self.sample_density.setObjectName("sample_density")
        self.diffractometer_settings_list.addWidget(self.sample_density, 3, 2, 1, 1)
        self.left_side.addLayout(self.diffractometer_settings_list)
        self.gridLayout_2.addLayout(self.left_side, 0, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.mplwindow = QtGui.QWidget(self.centralwidget)
        self.mplwindow.setObjectName("mplwindow")
        self.verticalLayout.addWidget(self.mplwindow)
        self.mplvl = QtGui.QVBoxLayout()
        self.mplvl.setObjectName("mplvl")
        self.verticalLayout.addLayout(self.mplvl)
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 21))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuTest = QtGui.QMenu(self.menubar)
        self.menuTest.setObjectName("menuTest")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menu_openpattern = QtGui.QAction(MainWindow)
        self.menu_openpattern.setObjectName("menu_openpattern")
        self.menuTest.addAction(self.menu_openpattern)
        self.menubar.addAction(self.menuTest.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fitting_params.setText(QtGui.QApplication.translate("MainWindow", "Fitting Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.enable_all_button.setText(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.enable_none_button.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.enable_invert_button.setText(QtGui.QApplication.translate("MainWindow", "Invert", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_02.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_03.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_12.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_15.setText(QtGui.QApplication.translate("MainWindow", "Pt, Probability of 3R Stacking", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_17.setText(QtGui.QApplication.translate("MainWindow", "PO, Preferential Orientation Factor", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_14.setText(QtGui.QApplication.translate("MainWindow", "Pr, Probability of Random Stacking", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_11.setText(QtGui.QApplication.translate("MainWindow", "SM, Width of M Distribution", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_09.setText(QtGui.QApplication.translate("MainWindow", "La, Coherence Length", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_03.setText(QtGui.QApplication.translate("MainWindow", "Background S^2", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_10.setText(QtGui.QApplication.translate("MainWindow", "M, Number of Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_02.setText(QtGui.QApplication.translate("MainWindow", "Background S", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_01.setText(QtGui.QApplication.translate("MainWindow", "Background Constant", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_09.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_10.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_14.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_01.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_13.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_15.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_17.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_06.setText(QtGui.QApplication.translate("MainWindow", "Background 1/S", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_05.setText(QtGui.QApplication.translate("MainWindow", "Background S^4", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_04.setText(QtGui.QApplication.translate("MainWindow", "Background S^3", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_08.setText(QtGui.QApplication.translate("MainWindow", "d002, Interlayer Spacing (Angstrom)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_12.setText(QtGui.QApplication.translate("MainWindow", "DAB, In plane strain", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_07.setText(QtGui.QApplication.translate("MainWindow", "A, In Plane Cell Constant (Angstrom)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_16.setText(QtGui.QApplication.translate("MainWindow", "Debye Waller Temperature Factor, (Angstrom^2)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_13.setText(QtGui.QApplication.translate("MainWindow", "del, Inter Plane Strain", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_00.setText(QtGui.QApplication.translate("MainWindow", "Scale Factor (a.u.)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_08.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_00.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_16.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_11.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_04.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_06.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_07.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_05.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fitting_settings.setText(QtGui.QApplication.translate("MainWindow", "Fitting Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Data Point Multiple (Nskip)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Integration Width (Nsg)", None, QtGui.QApplication.UnicodeUTF8))
        self.theta_min_label.setText(QtGui.QApplication.translate("MainWindow", "Theta Min", None, QtGui.QApplication.UnicodeUTF8))
        self.theta_max_label.setText(QtGui.QApplication.translate("MainWindow", "Theta Max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Stop Criteria (Epsilon)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Model Layers (1 or 2)", None, QtGui.QApplication.UnicodeUTF8))
        self.number_layers.setItemText(0, QtGui.QApplication.translate("MainWindow", "1 Layer Model", None, QtGui.QApplication.UnicodeUTF8))
        self.number_layers.setItemText(1, QtGui.QApplication.translate("MainWindow", "2 Layer Model", None, QtGui.QApplication.UnicodeUTF8))
        self.gradient_check_enable.setItemText(0, QtGui.QApplication.translate("MainWindow", "Off", None, QtGui.QApplication.UnicodeUTF8))
        self.gradient_check_enable.setItemText(1, QtGui.QApplication.translate("MainWindow", "On", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Iterations", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "TCI Points (NPhi)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Gradient Checking", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Gradient Checking Delta", None, QtGui.QApplication.UnicodeUTF8))
        self.label_diffractometer_settings.setText(QtGui.QApplication.translate("MainWindow", "Diffractometer Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Sample Depth (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("MainWindow", "Sample Density Fraction", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Sample Width (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "Beam Width (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Wavelength (Angstrom)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "Goniometer Radius (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTest.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_openpattern.setText(QtGui.QApplication.translate("MainWindow", "Open XRD Pattern", None, QtGui.QApplication.UnicodeUTF8))

