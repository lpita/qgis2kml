# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgis2kml.ui'
#
# Created: Tue Jun 26 21:38:50 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_qgis2kml(object):
    def setupUi(self, qgis2kml):
        qgis2kml.setObjectName(_fromUtf8("qgis2kml"))
        qgis2kml.resize(511, 346)
        self.buttonBox = QtGui.QDialogButtonBox(qgis2kml)
        self.buttonBox.setGeometry(QtCore.QRect(160, 310, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(qgis2kml)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 280, 491, 28))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.kmldirpath = QtGui.QLineEdit(self.layoutWidget)
        self.kmldirpath.setObjectName(_fromUtf8("kmldirpath"))
        self.horizontalLayout_3.addWidget(self.kmldirpath)
        self.browseButton = QtGui.QPushButton(self.layoutWidget)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout_3.addWidget(self.browseButton)
        self.layoutWidget_2 = QtGui.QWidget(qgis2kml)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 90, 491, 22))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_10.setMargin(0)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_3 = QtGui.QLabel(self.layoutWidget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_10.addWidget(self.label_3)
        self.label_29 = QtGui.QLabel(self.layoutWidget_2)
        self.label_29.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.horizontalLayout_10.addWidget(self.label_29)
        self.outputFormCombo = QtGui.QComboBox(self.layoutWidget_2)
        self.outputFormCombo.setObjectName(_fromUtf8("outputFormCombo"))
        self.outputFormCombo.addItem(_fromUtf8(""))
        self.outputFormCombo.addItem(_fromUtf8(""))
        self.horizontalLayout_10.addWidget(self.outputFormCombo)
        self.layoutWidget_3 = QtGui.QWidget(qgis2kml)
        self.layoutWidget_3.setGeometry(QtCore.QRect(0, 10, 471, 72))
        self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.layoutWidget_3)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2kml/icon.png")))
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Trebuchet MS"))
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_5 = QtGui.QLabel(self.layoutWidget_3)
        self.label_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.tablelayers = QtGui.QTableWidget(qgis2kml)
        self.tablelayers.setGeometry(QtCore.QRect(10, 120, 491, 151))
        self.tablelayers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tablelayers.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tablelayers.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.tablelayers.setObjectName(_fromUtf8("tablelayers"))
        self.tablelayers.setColumnCount(0)
        self.tablelayers.setRowCount(0)
        self.tablelayers.verticalHeader().setVisible(False)

        self.retranslateUi(qgis2kml)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), qgis2kml.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), qgis2kml.reject)
        QtCore.QMetaObject.connectSlotsByName(qgis2kml)

    def retranslateUi(self, qgis2kml):
        qgis2kml.setWindowTitle(QtGui.QApplication.translate("qgis2kml", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("qgis2kml", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("qgis2kml", "OGR active layers :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_29.setText(QtGui.QApplication.translate("qgis2kml", "OGR output format", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFormCombo.setItemText(0, QtGui.QApplication.translate("qgis2kml", "KML", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFormCombo.setItemText(1, QtGui.QApplication.translate("qgis2kml", "KMZ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("qgis2kml", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Trebuchet MS\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">qgis2kml</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("qgis2kml", "Export active layers to KML/KMZ consider the style of layer", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
