from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*


class ConfirmWindow(QMessageBox):  #creates a class window
    def __init__(self,parentWindow,message):
        super().__init__()     #use super class of QMainWindow
        self.message = message
        self.parentWindow = parentWindow
        self.initUI()
    def initUI(self):   #create UI

        self.setWindowTitle("Alert!")
        self.setText(self.message)
        self.setIcon(QMessageBox.Question)

        self.confirm = self.buttonClicked.connect(self.confirmClicked)

        self.cancelButton = QPushButton(self)
        self.cancelButton.clicked.connect(self.cancelClicked)
        self.cancelButton.setText("Cancel")
        self.cancelButton.move(140,60)
        self.cancelButton.resize(75,20)

        x = self.exec_()

    def confirmClicked(self):
        self.parentWindow.removeConfirmed = True
        self.close()

    def cancelClicked(self):
        self.parentWindow.removeConfirmed = False
        self.close()

    def closeEvent(self):
        self.parentWindow.removeConfirmed = False
        self.close()
