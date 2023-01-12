# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'warning.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_warnDialog(object):
    def setupUi(self, warnDialog):
        warnDialog.setObjectName("warnDialog")
        warnDialog.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(warnDialog)
        self.pushButton.setGeometry(QtCore.QRect(220, 220, 152, 43))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(warnDialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 271, 131))
        self.label.setObjectName("label")

        self.retranslateUi(warnDialog)
        self.pushButton.clicked.connect(warnDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(warnDialog)

    def retranslateUi(self, warnDialog):
        _translate = QtCore.QCoreApplication.translate
        warnDialog.setWindowTitle(_translate("warnDialog", "Warning"))
        self.pushButton.setText(_translate("warnDialog", "OK"))
        self.label.setText(_translate("warnDialog", "Task and time not set!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    warnDialog = QtWidgets.QDialog()
    ui = Ui_warnDialog()
    ui.setupUi(warnDialog)
    warnDialog.show()
    sys.exit(app.exec_())

