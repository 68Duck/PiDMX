from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from pydmx import PyDMX
from messageWindow import MessageWindow

class PortSelectionWindow(QMainWindow,uic.loadUiType(os.path.join("ui","portSelectionWindow.ui"))[0]):
    def __init__(self,parentWindow):
        super().__init__()
        self.parentWindow = parentWindow
        self.setupUi(self)
        self.setWindowTitle("Port Selection")
        self.submitButton.clicked.connect(self.submitButtonPressed)
        self.testPortButton.clicked.connect(self.testButtonPressed)
        self.show()

    def submitButtonPressed(self):
        port = self.getPort()
        self.parentWindow.runComputerDMX(port)
        self.close()

    def testButtonPressed(self):
        port = self.getPort()
        dmx = PyDMX(port)
        if dmx.working:
            self.messageWindow = MessageWindow("The port works with DMX")
        else:
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
            self.submitButtonPressed()
