from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from errorWindow import ErrorWindow

class SequencePlaybackWindow(QWidget,uic.loadUiType("SequencePlaybackWindow.ui")[0]):
    def __init__(self,dataBaseManager,sequenceWindow):
        super().__init__()
        self.setupUi(self)
        self.dataBaseManager = dataBaseManager
        self.sequenceWindow = sequenceWindow
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Save Playback")

        self.confirmButton.clicked.connect(self.confirmButtonPressed)

    def confirmButtonPressed(self):
        self.timeDelay = self.timeDelayInput.text()
        self.playbackName = self.nameInput.text()
        sequenceInformation = self.dataBaseManager.getAllData("sequence"+str(self.sequenceWindow.sequenceID))
        for record in sequenceInformation:
            if record[3] == self.playbackName:
                self.errorWindow = ErrorWindow("There is already a playback with that name. Please input a different name.")
                return
        try:
            self.timeDelay = float(self.timeDelay)
            timeDelayValid = True
        except:
            self.errorWindow = ErrorWindow("The time you have inputed is not valid. Please try again")
            timeDelayValid = False
        if timeDelayValid:
            self.savePlayback()
        self.close()

    def savePlayback(self):
        nextPlaybackID = self.getNextSequencePlaybackID()
        self.dataBaseManager.createSequencePlaybackTable(nextPlaybackID)
        self.dataBaseManager.insertRecord("sequence"+str(self.sequenceWindow.sequenceID),[None,nextPlaybackID,self.timeDelay,self.playbackName])
        for light in self.sequenceWindow.displayLights:
            channelNumber = int(light.lightName[len(light.lightType):len(light.lightName)])
            if light.lightType == "GenericDimmer":
                for fixture in self.sequenceWindow.lightDisplay.lights:
                    if channelNumber == fixture.startChannel:
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber,fixture.intensity])
            elif light.lightType == "RGBLight" or light.lightType == "RGB6Channel":
                self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber,255])
                channelNumber += 1
                self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber,light.red])
                self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,int(channelNumber)+1,light.green])
                self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,int(channelNumber)+2,light.blue])
            elif light.lightType == "Miniscan":
                for fixture in self.sequenceWindow.lightDisplay.lights:
                    if channelNumber == fixture.startChannel:
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber,fixture.colour])
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber+1,fixture.goboRoation])
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber+2,fixture.gobo])
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber+3,fixture.intensity])
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber+4,fixture.pan])
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber+5,fixture.tilt])
                        self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber+6,fixture.effects])

            else:
                self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,channelNumber,light.red])
                self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,int(channelNumber)+1,light.green])
                self.dataBaseManager.insertRecord("sequencePlayback"+str(nextPlaybackID),[None,int(channelNumber)+2,light.blue])
        savedPlaybacks = self.dataBaseManager.getAllData("sequence"+str(self.sequenceWindow.sequenceID))
        self.sequenceWindow.displayingPlaybackID = len(savedPlaybacks)

    def getNextSequencePlaybackID(self):
        exisits = True
        counter = 0
        while exisits:
            exisits = self.dataBaseManager.checkIfTableExisits("sequencePlayback"+str(counter))
            counter += 1
        counter -= 1 #as the last one didn't exist so this is the next one
        return counter
