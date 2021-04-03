from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class ChooseLightForSequenceWindow(QWidget,uic.loadUiType("chooseLightForSequenceWindow.ui")[0]):
    def __init__(self,sequenceWindow):
        super().__init__()
        self.setupUi(self)
        self.sequenceWindow = sequenceWindow
        self.setWindowTitle("Choose Light")
        self.initUI()

    def initUI(self):
        # self.dropDown = QComboBox(self)
        # self.dropDown.move(50,50)
        # self.dropDown.setMinimumWidth(200)
        for light in self.sequenceWindow.lightsToPlace:
            self.dropDown.addItem(light.lightType+""+str(light.channelNumber))

        # self.addLightButton = QPushButton(self)
        # self.addLightButton.setFixedWidth(100)
        # self.addLightButton.move(200,200)
        # self.addLightButton.setText("Add Light")
        # self.addLightButton.setStyleSheet("background-color:white")
        self.addLightButton.clicked.connect(self.addLightButtonClicked)

    def addLightButtonClicked(self):
        lightSelectedName = self.dropDown.currentText()
        for light in self.sequenceWindow.lights:
            if lightSelectedName == light.lightType+""+str(light.channelNumber):
                self.sequenceWindow.addingLight = lightSelectedName
                self.sequenceWindow.addingLightType = light.lightType
                self.sequenceWindow.lightsToPlace.remove(light)
        self.close()
