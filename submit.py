# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'submit.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_submitDialog(object):
    def setupUi(self, submitDialog):
        submitDialog.setObjectName("submitDialog")
        submitDialog.resize(494, 318)
        self.submitBox = QtWidgets.QDialogButtonBox(submitDialog)
        self.submitBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.submitBox.setOrientation(QtCore.Qt.Horizontal)
        self.submitBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.submitBox.setCenterButtons(False)
        self.submitBox.setObjectName("submitBox")
        self.submitLabel = QtWidgets.QLabel(submitDialog)
        self.submitLabel.setGeometry(QtCore.QRect(40, 20, 421, 181))
        self.submitLabel.setText("")
        self.submitLabel.setWordWrap(True)
        self.submitLabel.setObjectName("submitLabel")

        self.retranslateUi(submitDialog)
        self.submitBox.accepted.connect(submitDialog.accept)
        self.submitBox.rejected.connect(submitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(submitDialog)

    def retranslateUi(self, submitDialog):
        _translate = QtCore.QCoreApplication.translate
        submitDialog.setWindowTitle(_translate("submitDialog", "Submit Request"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    submitDialog = QtWidgets.QDialog()
    ui = Ui_submitDialog()
    ui.setupUi(submitDialog)
    submitDialog.show()
    sys.exit(app.exec_())

