from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

class ChooseLightForSequenceWindow(QWidget,uic.loadUiType(os.path.join("ui","chooseLightForSequenceWindow.ui"))[0]):
    def __init__(self,sequenceWindow):
        super().__init__()
        self.setupUi(self)
        self.sequenceWindow = sequenceWindow
        self.setWindowTitle("Choose Light")
        self.initUI()

    def initUI(self):
        for light in self.sequenceWindow.lightsToPlace:
            self.dropDown.addItem(light.lightType+""+str(light.channelNumber))

        self.addLightButton.clicked.connect(self.addLightButtonClicked)

    def addLightButtonClicked(self):
        lightSelectedName = self.dropDown.currentText()
        for light in self.sequenceWindow.lights:
            if lightSelectedName == light.lightType+""+str(light.channelNumber):
                self.sequenceWindow.addingLight = lightSelectedName
                self.sequenceWindow.addingLightType = light.lightType
                self.sequenceWindow.lightsToPlace.remove(light)
        self.close()
