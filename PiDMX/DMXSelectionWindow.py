from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from pydmx import PyDMX
from messageWindow import MessageWindow
from errorWindow import ErrorWindow

class DMXSelectionWindow(QMainWindow,uic.loadUiType(os.path.join("ui","DMXSelectionWindow.ui"))[0]):
    def __init__(self,parentWindow):
        super().__init__()
        self.parentWindow = parentWindow
        self.setupUi(self)
        self.setWindowTitle("DMX Selection Window")
        self.raspberryPiPasswordInput.setEchoMode(QLineEdit.Password)
        self.raspberryPiSubmitButton.clicked.connect(self.raspberryPiSubmitButtonPressed)
        self.computerDMXSubmitButton.clicked.connect(self.computerDMXSubmitButtonPressed)
        self.testPortButton.clicked.connect(self.testButtonPressed)
        self.runWithoutDMXButton.clicked.connect(self.runWithoutDMX)

    def runWithoutDMX(self):
        self.parentWindow.runWithoutDMX()
        self.close()

    def raspberryPiSubmitButtonPressed(self):
        self.password = self.raspberryPiPasswordInput.text()
        self.parentWindow.login(self.password)

    def computerDMXSubmitButtonPressed(self):
        port = self.getPort()
        print(port)
        try:
            dmx = PyDMX(port)
            if dmx.working:
                del dmx
                self.parentWindow.runComputerDMX(port)
                self.close()
            else:
                raise Exception("The dmx is not working")
        except Exception as e:
            print(e)
            self.messageWindow = ErrorWindow("The port does NOT work with DMX")

    def testButtonPressed(self):
        port = self.getPort()
        print(port)
        try:
            dmx = PyDMX(port)
            if dmx.working:
                self.messageWindow = MessageWindow("The port works with DMX")
        except Exception as e:
            self.messageWindow = MessageWindow("The port does NOT work with DMX")

    def getPort(self):
        port = self.portSelectionInput.value()
        if self.windowsRadio.isChecked():
            port = f"COM{port}"
        if self.linuxRadio.isChecked():
            port = f"/dev/ttyUSB{port}"
        return port


    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Return:
            if self.tabWidget.currentIndex() == 0:
                self.raspberryPiSubmitButtonPressed()
            elif self.tabWidget.currentIndex() == 1:
                self.computerDMXSubmitButtonPressed()
            elif self.tabWidget.currentIndex() == 2:
                self.runWithoutDMX()
            else:
                self.errorWindow = ErrorWindow("The program should never reach here.")
        if e.key() == Qt.Key_1:
            self.tabWidget.setCurrentIndex(0)
        if e.key() == Qt.Key_2:
            self.tabWidget.setCurrentIndex(1)
        if e.key() == Qt.Key_3:
            self.tabWidget.setCurrentIndex(2)
