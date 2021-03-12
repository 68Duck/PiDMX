from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class RaspberryPiLoginWindow(QMainWindow,uic.loadUiType("raspberryPiLoginWindow.ui")[0]):
    def __init__(self,parentWindow):
        super().__init__()
        self.parentWindow = parentWindow
        self.setupUi(self)
        self.setWindowTitle("Raspberry Pi Login")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.submitButton.clicked.connect(self.submitButtonPressed)
        self.runOnComputerAction.triggered.connect(self.runComputerDMX)
        self.runWithoutDMXAction.triggered.connect(self.runWithoutDMX)

    def runComputerDMX(self):
        self.parentWindow.runComputerDMX()
        self.close()

    def runWithoutDMX(self):
        self.parentWindow.runWithoutDMX()
        self.close()

    def submitButtonPressed(self):
        self.password = self.passwordInput.text()
        self.parentWindow.login()

    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Return:
            self.submitButtonPressed()
