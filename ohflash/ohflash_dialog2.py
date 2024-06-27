# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ohflash_dialog2.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtGui import QIntValidator


class Ui_OHFlashDialog2(object):
    def setupUi(self, OHFlashDialog2):
        OHFlashDialog2.setObjectName("OHFlashDialog2")
        OHFlashDialog2.resize(458, 204)
        OHFlashDialog2.setMinimumSize(QtCore.QSize(458, 204))
        OHFlashDialog2.setMaximumSize(QtCore.QSize(458, 204))
        self.layoutWidget = QtWidgets.QWidget(OHFlashDialog2)
        self.layoutWidget.setGeometry(QtCore.QRect(13, 13, 431, 182))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.optionsComboBox = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.optionsComboBox.setFont(font)
        self.optionsComboBox.setEditable(False)
        self.optionsComboBox.setCurrentText("")
        self.optionsComboBox.setObjectName("optionsComboBox")
        self.gridLayout.addWidget(self.optionsComboBox, 1, 0, 1, 2)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.zoomScale = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.zoomScale.setFont(font)
        self.zoomScale.setText("")
        self.zoomScale.setClearButtonEnabled(True)
        self.zoomScale.setObjectName("zoomScale")

        int_validator = QIntValidator()
        self.zoomScale.setValidator(int_validator)

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.zoomScale)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.LabelRole, self.formLayout)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.NumValue = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumValue.setFont(font)
        self.NumValue.setText("")
        self.NumValue.setClearButtonEnabled(True)
        self.NumValue.setObjectName("NumValue")

        self.NumValue.setValidator(int_validator)
        
        self.horizontalLayout.addWidget(self.NumValue)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)
        self.gridLayout.addLayout(self.formLayout_2, 2, 0, 1, 2)
        self.okButtonOptions = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.okButtonOptions.setFont(font)
        self.okButtonOptions.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.okButtonOptions.setObjectName("okButtonOptions")
        self.gridLayout.addWidget(self.okButtonOptions, 3, 1, 1, 1)

        self.retranslateUi(OHFlashDialog2)
        QtCore.QMetaObject.connectSlotsByName(OHFlashDialog2)
        OHFlashDialog2.setTabOrder(self.optionsComboBox, self.NumValue)
        OHFlashDialog2.setTabOrder(self.NumValue, self.zoomScale)
        OHFlashDialog2.setTabOrder(self.zoomScale, self.okButtonOptions)

    def retranslateUi(self, OHFlashDialog2):
        _translate = QtCore.QCoreApplication.translate
        OHFlashDialog2.setWindowTitle(_translate("OHFlashDialog2", "Dialog"))
        self.label.setText(_translate("OHFlashDialog2", "Choisissez un mode de traitement"))
        self.label_3.setText(_translate("OHFlashDialog2", "Choisissez l\'échelle du zoom (ex : 500 pour 1:500)"))
        self.zoomScale.setPlaceholderText(_translate("OHFlashDialog2", "Entrez un nombre"))
        self.label_2.setText(_translate("OHFlashDialog2", "Choisissez le nombre de valeurs à utiliser lors du traitement"))
        self.NumValue.setPlaceholderText(_translate("OHFlashDialog2", "Entrez un nombre"))
        self.okButtonOptions.setText(_translate("OHFlashDialog2", "OK"))
