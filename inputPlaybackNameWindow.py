from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class InputPlaybackNameWindow(QMessageBox):
    def __init__(self,message,windowTitle,visualLightDisplay):
        self.visualLightDisplay = visualLightDisplay
        self.message = message
        self.windowTitle = windowTitle
        super().__init__()     #use super class
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.windowTitle)
        self.setText(self.message)
        self.setIcon(QMessageBox.Question)

        self.inputBox = QLineEdit(self)
        self.inputBox.move(100,40)
        self.inputBox.setPlaceholderText("Enter here")

        self.inputButton = self.buttonClicked.connect(self.buttonPressed)

        x=self.exec_()

    def buttonPressed(self):
        self.visualLightDisplay.playbackName = self.inputBox.text()
