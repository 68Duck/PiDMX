from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class OpenRigWindow(QWidget):
    def __init__(self,dataBaseManager,lightDisplay,visualLightDisplay):
        super().__init__()
        self.visualLightDisplay = visualLightDisplay
        self.lightDisplay = lightDisplay
        self.dataBaseManager = dataBaseManager
        self.rigOpened = False
        self.removeConfirmed = False
        self.setWindowTitle("Open Rig")
        self.initUI()

    def initUI(self):
        self.openButton = QPushButton(self)
        self.openButton.move(300,200)
        self.openButton.setFixedWidth(100)
        self.openButton.setText("Open")
        self.openButton.clicked.connect(self.openButtonClicked)

        self.deleteButton = QPushButton(self)
        self.deleteButton.move(300,100)
        self.deleteButton.setFixedWidth(100)
        self.deleteButton.setText("Delete Table")
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        self.savedRigs = self.dataBaseManager.getAllData("LightingRigs")

        self.dropDown = QComboBox(self)
        self.dropDown.move(50,50)
        self.dropDown.setMinimumWidth(200)
        for rig in self.savedRigs:
            self.dropDown.addItem(rig[1])  #rig[1] is the name of the rig

    def deleteButtonClicked(self):
        confirmWindow = ConfirmWindow(self,True)
        if self.removeConfirmed:
            rigToDelete = self.dropDown.currentText()
            if rigToDelete == "":
                self.errorWindow = ErrorWindow("This rig does not exisit. Try saving a rig before trying to delete one.")
            else:
                self.dataBaseManager.deleteRigFromLightingRigs(rigToDelete)
                for rig in self.savedRigs:
                    if rigToDelete == rig[1]:
                        rigID = rig[2]
                self.dataBaseManager.dropRigTable(rigID)
            self.close()

    def openButtonClicked(self):
        self.rig = self.dropDown.currentText()
        self.rigID = False
        for rig in self.savedRigs:
            if self.rig == rig[1]:
                self.rigID = rig[2]
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
        for light in self.lightDisplay.lights:
            self.lightDisplay.lights.remove(light)
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
                lightType = light[1]
                xpos = light[2]
                ypos = light[3]
                startChannel = light[4]
                lightInformation = self.getLightInformation(lightType)
                self.newLight = lightInformation.generateNewLight(startChannel)
                self.newLight.lightDisplay = self.lightDisplay
                self.newLight.changeUniverse()
                self.lightDisplay.lights.append(self.newLight)
                self.lightDisplay.updateOccupiedChannels()
                self.displayOnWindow(self.newLight,xpos,ypos,lightType,startChannel)

    def displayOnWindow(self,light,xpos,ypos,lightType,channel):
        self.visualLightDisplay.createLightFromSavedRig(light,xpos,ypos,lightType,channel)

    def getLightInformation(self,lightType):
        for light in self.lightDisplay.lightsInformation:
            if light.lightType == lightType:
                return light
        self.errorWindow = ErrorWindow("Something went wrong with getting the light information.")
        return False
