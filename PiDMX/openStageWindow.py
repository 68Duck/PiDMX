from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from databaseManager import DataBaseManager

class OpenStageWindow(QWidget,uic.loadUiType(os.path.join("ui","openStageWindow.ui"))[0]):
    def __init__(self,lightDisplayWindow):
        super().__init__()
        self.setupUi(self)
        self.lightDisplayWindow = lightDisplayWindow
        self.setWindowTitle("Choose Stage")
        self.initUI()
        self.show()

    def initUI(self):
        self.dataBaseManager = DataBaseManager("bars.db")
        self.locations = self.dataBaseManager.getAllData("locations")
        for location in self.locations:
            self.dropDown.addItem(location["locationName"])

        self.openStageButton.clicked.connect(self.openStageButtonClicked)

    def openStageButtonClicked(self):
        self.location = self.dropDown.currentText()
        self.lightDisplayWindow.openStage(self.location)
        self.close()
