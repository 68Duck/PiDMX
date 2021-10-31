from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from confirmWindow import ConfirmWindow
from errorWindow import ErrorWindow

class OpenRigWindow(QWidget,uic.loadUiType(os.path.join("ui","openRigWindow.ui"))[0]):
    def __init__(self,dataBaseManager,lightDisplay,visualLightDisplay):
        super().__init__()
        self.setupUi(self)
        self.visualLightDisplay = visualLightDisplay
        self.lightDisplay = lightDisplay
        self.dataBaseManager = dataBaseManager
        self.rigOpened = False
        self.removeConfirmed = False
        self.setWindowTitle("Open Rig")
        self.initUI()

    def initUI(self):
        self.openButton.clicked.connect(self.openButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.savedRigs = self.dataBaseManager.getAllData("LightingRigs")
        for rig in self.savedRigs:
            self.dropDown.addItem(rig["name"])

    def deleteButtonClicked(self):
        confirmWindow = ConfirmWindow(self,"Are you sure you want to remove this rig?")
        if self.removeConfirmed:
            rigToDelete = self.dropDown.currentText()
            if rigToDelete == "":
                self.errorWindow = ErrorWindow("This rig does not exisit. Try saving a rig before trying to delete one.")
            else:
                self.dataBaseManager.deleteRigFromLightingRigs(rigToDelete)
                for rig in self.savedRigs:
                    if rigToDelete == rig["name"]:
                        rigID = rig["lightsTableID"]
                self.dataBaseManager.dropRigTable(rigID)
            self.close()

    def openButtonClicked(self):
        self.rig = self.dropDown.currentText()
        self.rigID = False
        for rig in self.savedRigs:
            if self.rig == rig["name"]:
                self.rigID = rig["lightsTableID"]
        if self.rigID == False and self.rigID != 0:
            self.rigOpened = False
            self.errorWindow = ErrorWindow("This rig does not exist. Try saving a rig first")
        else:
            self.rigToOpen = self.dataBaseManager.getAllData("rig"+str(self.rigID))
            if self.rigToOpen == False:
                self.errorWindow = ErrorWindow("The rig you have selected does not exist. Please try again")
            else:
                self.closeRig()
                self.openRig()
                self.rigOpened = True

        self.close()

    def closeRig(self):
        # print("test")
        # print(self.lightDisplay.lights)
        # for light in self.lightDisplay.lights:
        #     self.lightDisplay.lights.remove(light)
        # print(self.lightDisplay.lights)
        self.lightDisplay.lights = []
        self.lightDisplay.updateOccupiedChannels()
        self.lightDisplay.createBlankUniverse()
        for i in range(len(self.visualLightDisplay.lightList)):
            self.visualLightDisplay.removeLight(self.visualLightDisplay.lightList[0])
        if self.lightDisplay.runningChaser == True:
            self.visualLightDisplay.effectsWindow.toggleChaser()
        if self.lightDisplay.runningRainbow == True:
            self.visualLightDisplay.effectsWindow.toggleRainbow()

    def closeEvent(self,*args,**kargs):
        if self.rigOpened:
            self.visualLightDisplay.openWindowClosed()


    def openRig(self):
        if self.rigToOpen == False:
            self.errorWindow = ErrorWindow("The rig you have selected does not exist. Please try again")
        else:
            for light in self.rigToOpen:
                # print(light)
                lightType = light["lightType"]
                xpos = light["xPos"]
                ypos = light["yPos"]
                startChannel = light["startChannel"]
                lightInformation = self.getLightInformation(lightType)
                # print(lightInformation)
                self.newLight = lightInformation.generateNewLight(startChannel)
                self.newLight.lightDisplay = self.lightDisplay
                self.newLight.changeUniverse(updateUniverse = False)
                self.lightDisplay.lights.append(self.newLight)
                self.lightDisplay.updateOccupiedChannels()
                self.displayOnWindow(self.newLight,xpos,ypos,lightType,startChannel)
            self.lightDisplay.universeChanged()

    def displayOnWindow(self,light,xpos,ypos,lightType,channel):
        self.visualLightDisplay.createLightFromSavedRig(light,xpos,ypos,lightType,channel)

    def getLightInformation(self,lightType):
        for light in self.lightDisplay.lightsInformation:
            if light.lightType == lightType:
                return light
        self.errorWindow = ErrorWindow("Something went wrong with getting the light information.")
        return False
