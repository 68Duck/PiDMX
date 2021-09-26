from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from errorWindow import ErrorWindow

class SequenceSelectionWindow(QWidget,uic.loadUiType(os.path.join("ui","sequenceSelectionWindow.ui"))[0]):
    def __init__(self,dataBaseManager,lightDisplay,visualLightDisplay):
        super().__init__()
        self.setupUi(self)
        self.dataBaseManager = dataBaseManager
        self.lightDisplay = lightDisplay
        self.visualLightDisplay = visualLightDisplay
        self.loopSequence = False
        self.setWindowTitle("Choose Sequence")
        self.initUI()

    def initUI(self):
        self.openButton.clicked.connect(self.openButtonClicked)
        self.savedSequences = self.dataBaseManager.getAllData("Sequences")
        for sequence in self.savedSequences:
            if self.visualLightDisplay.rigID == sequence["rigID"]:  #checks is the rigID is the same
                self.dropDown.addItem(sequence["sequenceName"])  #sequence[2] is the name of the sequence


    def openButtonClicked(self):
        self.moveOnSpace = self.spacebarCheckBox.isChecked()
        self.loopSequence = self.loopCheckBox.isChecked()
        self.sequence = self.dropDown.currentText()
        self.visualLightDisplay.runningSequence = True
        self.setupSequence()

    def setupSequence(self):
        self.sequenceCreatorID = False
        for sequence in self.savedSequences:
            if self.sequence == sequence["sequenceName"]:
                self.sequenceCreatorID = sequence["sequenceCreatorID"]
                self.sequenceID = sequence["sequenceID"]
        if self.sequenceCreatorID == False and self.sequenceCreatorID != 0:
            self.sequenceOpened = False
            self.errorWindow = ErrorWindow("This rig does not exist. Try saving a rig first")
        else:
            self.sequenceToOpen = self.dataBaseManager.getAllData("sequence"+str(self.sequenceCreatorID))
            if self.sequenceToOpen == False:
                self.errorWindow = ErrorWindow("The sequence you have selected does not exist. Please try again")
            elif len(self.sequenceToOpen) == 0:
                self.errorWindow = ErrorWindow("There are no playbacks stored in that sequence. Please try again")
            else:
                self.close()
                self.closeEffects()
                self.runSequence()

    def closeEffects(self):
        if self.lightDisplay.runningChaser == True:
            self.visualLightDisplay.effectsWindow.toggleChaser()
        if self.lightDisplay.runningRainbow == True:
            self.visualLightDisplay.effectsWindow.toggleRainbow()
        for selectedLight in self.visualLightDisplay.selectedLights:
            selectedLight.toggleSelected()
            self.visualLightDisplay.selectedLights.remove(selectedLight)

    def runSequence(self):
        self.lightDisplay.universeLock = True
        self.lightDisplay.createBlankUniverse()
        for light in self.visualLightDisplay.lightList: #set all to unselected First
            if light.selected == True:
                light.toggleSelected()
        self.firstTimeDelay = self.sequenceToOpen[0]["timeDelay"]
        timeDelayTotal = self.sequenceToOpen[0]["timeDelay"] * -1  #negates the first one so opened immediately
        self.timers = []
        for sequence in self.sequenceToOpen:
            self.nextSequence = sequence
            timeDelay = sequence["timeDelay"]
            timeDelayTotal += timeDelay
            if self.moveOnSpace:
                self.visualLightDisplay.checkForSpace = True
                self.timers.append(1) #used to count the number of sequences so if needs to reset.
            else:
                self.newTimer = QTimer()
                self.newTimer.timeout.connect(self.openIndividualSequence)
                self.timers.append(self.newTimer)
                self.newTimer.start(int(timeDelayTotal*1000))

    def openIndividualSequence(self):
        sequence = self.sequenceToOpen[0]
        self.sequenceToOpen.pop(0)
        playbackID = sequence["playbackID"]
        timeDelay = sequence["timeDelay"]
        self.playbackToOpen = self.dataBaseManager.getAllData("sequencePlayback"+str(playbackID))
        for playback in self.playbackToOpen:
            channelNumber = int(playback["channelNumber"])
            channelValue = int(playback["channelValue"])
            self.lightDisplay.universeChannelValues[channelNumber] = channelValue
        for light in self.lightDisplay.lights:
            light.updateChannelValuesFromUniverse()
            light.updateChannelValues()
        self.lightDisplay.universeLock = False
        self.lightDisplay.universeChanged()
        for light in self.visualLightDisplay.lightList:
            light.changeColourAccordingToFixture()
        if self.moveOnSpace:
            self.visualLightDisplay.checkForSpace = True
        else:
            self.timers[0].stop()
        self.timers.pop(0)
        if len(self.timers) == 0:
            if self.loopSequence:
                if self.moveOnSpace:
                    self.setupSequence()
                else:
                    self.resetTimer = QTimer()
                    self.resetTimer.timeout.connect(self.replaySequence)
                    self.resetTimer.start(self.firstTimeDelay*1000) #*1000 as miliseconds
            else:
                if self.moveOnSpace:
                    self.visualLightDisplay.checkForSpace = False

    def replaySequence(self):
        self.resetTimer.stop()
        self.setupSequence()
