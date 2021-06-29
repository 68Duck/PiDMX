from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from errorWindow import ErrorWindow
from confirmWindow import ConfirmWindow

class OpenSequenceWindow(QWidget,uic.loadUiType(os.path.join("ui","openRigWindow.ui"))[0]):
    def __init__(self,dataBaseManager,sequenceWindow):
        super().__init__()
        self.setupUi(self)
        self.sequenceWindow = sequenceWindow
        self.dataBaseManager = dataBaseManager
        self.sequenceOpened = False
        self.removeConfirmed = False
        self.setWindowTitle("Open Sequence")
        self.initUI()

    def initUI(self):
        self.openButton.clicked.connect(self.openButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.savedSequences = self.dataBaseManager.getAllData("Sequences")
        for sequence in self.savedSequences:
            if self.sequenceWindow.rigID == sequence["rigID"]:
                self.dropDown.addItem(sequence["sequenceName"])

    def deleteButtonClicked(self):
        confirmWindow = ConfirmWindow(self,"Are you sure you want to remove this sequence?")
        if self.removeConfirmed:
            sequenceToDelete = self.dropDown.currentText()
            if sequenceToDelete == "":
                self.errorWindow = ErrorWindow("This sequence does not exisit. Try saving a sequence before trying to delete one.")
            else:
                self.dataBaseManager.deleteSequenceFromSequences(sequenceToDelete)
                for sequence in self.savedSequences:
                    if sequenceToDelete == sequence["sequenceName"]:
                        sequenceID = sequence["sequenceID"]
                        sequenceCreatorID = sequence["sequenceCreatorID"]
                self.dataBaseManager.dropSequenceTable(sequenceID)
                self.dataBaseManager.dropSequenceCreatorTable(sequenceCreatorID)
            self.close()

    def openButtonClicked(self):
        self.sequence = self.dropDown.currentText()
        self.sequenceCreatorID = False
        for sequence in self.savedSequences:
            if self.sequence == sequence["sequenceName"]:
                self.sequenceCreatorID = sequence["sequenceCreatorID"]
                self.sequenceID = sequence["sequenceID"]
        if self.sequenceCreatorID == False and self.sequenceCreatorID != 0:
            self.sequenceOpened = False
            self.errorWindow = ErrorWindow("This rig does not exist. Try saving a rig first")
        else:
            self.sequenceToOpen = self.dataBaseManager.getAllData("sequenceCreator"+str(self.sequenceCreatorID))
            if self.sequenceToOpen == False:
                self.errorWindow = ErrorWindow("The sequence you have selected does not exist. Please try again")
            else:
                self.closeSequence()
                self.openSequence()
                self.sequenceOpened = True
        self.close()

    def closeSequence(self):
        self.sequenceWindow.lightsToPlace = self.sequenceWindow.lights[:] #[:] creates a copy so the lists dont interact with each other
        for light in self.sequenceWindow.displayLights:
            light.remove()

    def closeEvent(self,*args,**kargs):
        if self.sequenceOpened:
            self.sequenceWindow.openWindowClosed()

    def openSequence(self):
        if self.sequenceToOpen == False:
            self.errorWindow = ErrorWindow("The sequence you have selected does not exist. Please try again")
        else:
            for light in self.sequenceToOpen:
                lightName = light["lightName"]
                lightType = light["lightType"]
                xPos = light["xPos"]
                yPos = light["yPos"]
                self.sequenceWindow.createLight(lightType,lightName,xPos,yPos,openFromSavedSequence=True)
                lightsAlreadyPlaced = []
                for l in self.sequenceWindow.lightsToPlace:
                    if lightName == l.lightType+""+str(l.channelNumber):
                        lightsAlreadyPlaced.append(l)
                for l in lightsAlreadyPlaced:
                    self.sequenceWindow.lightsToPlace.remove(l)
