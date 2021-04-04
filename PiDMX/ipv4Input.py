from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from pydmx import PyDMX
from messageWindow import MessageWindow

class IPv4Input(QMainWindow,uic.loadUiType(os.path.join("ui","ipv4Input.ui"))[0]):
    def __init__(self,parentWindow):
        super().__init__()
        self.parentWindow = parentWindow
        self.setupUi(self)
        self.setWindowTitle("IPv4 Input")
        self.submitButton.clicked.connect(self.submitButtonPressed)
        self.show()

    def submitButtonPressed(self):
        address = ""
        for i in range(1,5,1):
            number = str(getattr(self,f"portInput{i}").value())
            address = address + "." + number
        address = address[1:len(address)] #remvoes the . at the start
        self.parentWindow.connectToPi(address)
        self.close()


    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Return:
            self.submitButtonPressed()
