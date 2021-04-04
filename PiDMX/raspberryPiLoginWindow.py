from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from portSelectionWindow import PortSelectionWindow

class RaspberryPiLoginWindow(QMainWindow,uic.loadUiType(os.path.join("ui","raspberryPiLoginWindow.ui"))[0]):
    def __init__(self,parentWindow):
        super().__init__()
        self.parentWindow = parentWindow
        self.setupUi(self)
        self.setWindowTitle("Raspberry Pi Login")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.submitButton.clicked.connect(self.submitButtonPressed)
        self.runOnComputerAction.triggered.connect(self.runOnComputerActionTriggered)
        self.runWithoutDMXAction.triggered.connect(self.runWithoutDMX)

    def runOnComputerActionTriggered(self):
        self.portSelectionWindow = PortSelectionWindow(self)

    def runComputerDMX(self,port):
        self.parentWindow.runComputerDMX(port)
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
