from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from errorWindow import ErrorWindow

class LightTypeWindow(QWidget,uic.loadUiType(os.path.join("ui","lightTypeWindow.ui"))[0]):
    def __init__(self,parentWindow):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.parentWindow = parentWindow
        self.setWindowTitle("Select Light Type")
        self.initUI()
    def initUI(self):
        for light in self.parentWindow.lightDisplay.lightTypes:
            lightTypeInRig = False
            for l in self.parentWindow.lightList:
                if l.lightType == light:
                    lightTypeInRig = True
            if lightTypeInRig:
                self.dropDown.addItem(light)

        self.selectLightTypeButton.clicked.connect(self.selectLightTypeButtonClicked)

    def selectLightTypeButtonClicked(self):
        if self.selectLightsRadio.isChecked():
            select = True
        elif self.deselectLightsRadio.isChecked():
            select = False
        else:
            self.errorWindow = ErrorWindow("Error with selecting the lights. This should never be the case so is an error with the code.")
        self.parentWindow.selectLightsOfType(self.dropDown.currentText(),select)
        self.hide()
