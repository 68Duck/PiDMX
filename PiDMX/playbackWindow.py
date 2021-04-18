from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from errorWindow import ErrorWindow
from confirmWindow import ConfirmWindow

class PlaybackWindow(QWidget,uic.loadUiType(os.path.join("ui","playbackWindow.ui"))[0]):
    def __init__(self,visualLightDisplay,dataBaseManager,lightDisplay):
        super().__init__()
        self.setupUi(self)
        self.visualLightDisplay = visualLightDisplay
        self.dataBaseManager = dataBaseManager
        self.lightDisplay = lightDisplay
        # self.setGeometry(200,200,1000,800)
        self.setWindowTitle("Playbacks")
        self.initUI()

    def initUI(self):
        self.runButton.clicked.connect(self.runButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        self.savedPlaybacks = self.dataBaseManager.getCurrentRigsPlaybacks(self.visualLightDisplay.rigID)

        for playback in self.savedPlaybacks:
            self.dropDown.addItem(playback["Name"])  #playback[3] is the playback name

    def runButtonClicked(self):
        self.playback = self.dropDown.currentText()
        self.playbackID = None
        for playback in self.savedPlaybacks:
            if self.playback == playback["Name"]:
                self.playbackID = playback["PlaybackID"]
        if self.playbackID == None:
            self.playbackOpened = False
            self.errorWindow = ErrorWindow("This playback does not exist. Try creating a playback first")
        else:
            self.playbackToOpen = self.dataBaseManager.getAllData("playback"+str(self.playbackID))
            if self.playbackToOpen == False:
                self.errorWindow = ErrorWindow("This playback does not exist. Please try again")
            else:
                self.executePlayback()
                self.playbackOpened = True
        self.close()

    def executePlayback(self):
        self.lightDisplay.universeLock = True
        self.lightDisplay.createBlankUniverse()
        for light in self.visualLightDisplay.lightList: #set all to unselected First
            if light.selected == True:
                light.toggleSelected()
        if self.lightDisplay.runningChaser:
            self.visualLightDisplay.effectsWindow.toggleChaser()
        if self.lightDisplay.runningRainbow:
            self.visualLightDisplay.effectsWindow.toggleRainbow()
        for playback in self.playbackToOpen:
            channelNumber = playback["channelNumber"]
            channelValue = playback["channelValue"]
            try:
                channelNumber = int(channelNumber)
            except:
                pass
            if type(channelNumber) == int:
                self.lightDisplay.universeChannelValues[channelNumber] = channelValue
            elif channelNumber == "rainbow":
                if channelValue == 0:
                    self.lightDisplay.runningRainbow = False
                else:
                    self.visualLightDisplay.effectsWindow.rainbowDelay = channelValue
                    self.visualLightDisplay.effectsWindow.toggleRainbow()
                    self.visualLightDisplay.effectsWindow.rainbowIO[0].setChecked(True)
            elif channelNumber == "chaser":
                if channelValue == 0:
                    self.lightDisplay.runningChaser = False
                else:
                    self.visualLightDisplay.effectsWindow.chaserDelay = channelValue
                    self.visualLightDisplay.effectsWindow.toggleChaser()
            else: #so a selectedLight
                for light in self.visualLightDisplay.lightList:
                    if light.channelNumber == channelValue:
                        if light.selected == False:
                            light.toggleSelected()
                            self.visualLightDisplay.selectedLights.append(light)
                self.visualLightDisplay.effectsWindow.selectedLights = self.visualLightDisplay.selectedLights


        for light in self.lightDisplay.lights:
            light.updateChannelValuesFromUniverse()
            light.updateChannelValues()
        self.lightDisplay.universeLock = False
        self.lightDisplay.universeChanged()
        for light in self.visualLightDisplay.lightList:
            light.changeColourAccordingToFixture()



    def deleteButtonClicked(self):
        self.removedConfirmed = False
        confirmWindow = ConfirmWindow(self,"Are you sure you want to remove this playback?")
        if self.removeConfirmed:
            playbackToDelete = self.dropDown.currentText()
            if playbackToDelete == "":
                self.errorWindow = ErrorWindow("This playback does not exist.")
            else:
                self.dataBaseManager.dropPlaybackTable(self.visualLightDisplay.rigID,playbackToDelete)
                self.dataBaseManager.deletePlaybackFromPlaybacksTable(self.visualLightDisplay.rigID,playbackToDelete)
            self.close()
