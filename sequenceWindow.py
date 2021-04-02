from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from chooseLightForSequenceWindow import ChooseLightForSequenceWindow
from sequenceDisplayLightTypes import *
from saveSequenceWindow import SaveSequenceWindow
from openSequenceWindow import OpenSequenceWindow
from errorWindow import ErrorWindow
from sequencePlaybackWindow import SequencePlaybackWindow
from editSequenceWindow import EditSequenceWindow
from sliderPannelWindow import SliderPannelWindowSequenceWindow

class SequenceWindow(QMainWindow,uic.loadUiType("sequenceWindow.ui")[0]):
    def __init__(self,lightDisplay,visualLightDisplay,dataBaseManager,rigID):
        super().__init__()
        self.setupUi(self)
        self.rigID = rigID
        self.dataBaseManager = dataBaseManager
        self.visualLightDisplay = visualLightDisplay
        self.lights = self.visualLightDisplay.lightList
        self.lightsToPlace = self.lights[:]  #[:] creates a copy of the array
        self.lightDisplay = lightDisplay
        self.xpos = 0
        self.width = 1900
        self.ypos = 0
        self.height = 1000
        self.displayLights = []
        self.addingLight = False
        self.colourSelected = False
        self.colourModeSelected = False
        self.sequenceID = None
        self.displayingPlaybackID = 1
        self.playbacks = []  #for each subarray, [0] is the Playback ID and [1] is the timeDelay
        self.setGeometry(int(self.xpos),int(self.ypos),int(self.width),int(self.height)) #sets window parameters top left is (0,0)
        self.setWindowTitle("Lighting Sequence") #sets window title
        self.setStyleSheet("background-color:black;")
        self.initUI()
    def initUI(self):
        self.addLightButton.clicked.connect(self.addLightButtonClicked)
        self.selectColourButton.clicked.connect(self.selectColourButtonClicked)
        self.colourPickerButton.clicked.connect(self.colourPickerButtonClicked)
        self.saveSequenceButton.clicked.connect(self.saveSequenceButtonClicked)
        self.openButton.clicked.connect(self.openButtonClicked)
        self.autoSaveSequenceButton.clicked.connect(self.autoSaveSequenceButtonClicked)
        self.savePlaybackButton.clicked.connect(self.savePlaybackButtonClicked)
        self.nextPlaybackButton.clicked.connect(self.nextPlaybackButtonClicked)
        self.previousPlaybackButton.clicked.connect(self.previousPlaybackButtonClicked)
        self.colourReplaceButton.clicked.connect(self.colourReplaceButtonClicked)
        self.editSequenceButton.clicked.connect(self.editSequenceButtonClicked)
        self.addWholeRigButton.clicked.connect(self.addWholeRigButtonClicked)

    def addWholeRigButtonClicked(self):
        for light in self.lights:
            x,y=[light.xPos,light.yPos]
            lightName = light.lightType+""+str(light.channelNumber)
            self.createLight(light.lightType,lightName,x,y)
            self.lightsToPlace.remove(light)
        self.addWholeRigButton.setEnabled(False)

    def editSequenceButtonClicked(self):
        if self.sequenceID != None:
            self.editSequenceWindow = EditSequenceWindow(self.dataBaseManager,self)
            self.editSequenceWindow.show()
        else:
            self.errorWindow = ErrorWindow("You need to open or save a sequence before trying to edit one.")

    def colourReplaceButtonClicked(self):
        colourToReplace = QColorDialog.getColor()
        red = colourToReplace.red()
        green = colourToReplace.green()
        blue = colourToReplace.blue()
        newColour = QColorDialog.getColor()
        for light in self.displayLights:
            if light.red == red:
                if light.green == green:
                    if light.blue == blue:
                        red2 = newColour.red()
                        green2 = newColour.green()
                        blue2 = newColour.blue()
                        light.changeColourRGB(red=red2,green=green2,blue=blue2)

    def nextPlaybackButtonClicked(self):
        if self.sequenceID == None:
            self.errorWindow = ErrorWindow("You have not opened a sequence yet so you cannot move to the next playback.")
        else:
            self.displayingPlaybackID += 1
            sequenceData = self.dataBaseManager.getAllData("sequence"+str(self.sequenceID))
            if len(sequenceData) == 0:
                self.errorWindow = ErrorWindow("There are no playbacks in this sequence.")
                return
            elif len(sequenceData) < self.displayingPlaybackID:
                self.displayingPlaybackID = 1  #go back to the start
            self.openPlayback()

    def openPlayback(self):
        sequenceData = self.dataBaseManager.getAllData("sequence"+str(self.sequenceID))
        if len(sequenceData) > 0:
            playbackID = sequenceData[self.displayingPlaybackID-1][1]  #-1 as the first will be 0
        playbackData = self.dataBaseManager.getAllData("sequencePlayback"+str(playbackID))
        for record in playbackData:
            channel = int(record[1])
            channelValue = record[2]
            for displayLight in self.displayLights:
                displayLightChannel = int(displayLight.lightName[len(displayLight.lightType):len(displayLight.lightName)])
                if displayLight.lightType == "RGBLight" or displayLight.lightType == "RGB6Channel":
                    displayLightChannel+=1
                if int(displayLightChannel) == int(channel):
                    displayLight.changeColourRGB(red=channelValue)

                if int(displayLightChannel)+1 == int(channel):
                    displayLight.changeColourRGB(green=channelValue)
                if int(displayLightChannel)+2 == int(channel):
                    displayLight.changeColourRGB(blue=channelValue)
                if displayLight.lightType == "Miniscan":
                    for i in range(7):
                        if int(displayLightChannel+i) == int(channel):
                            self.lightDisplay.universeChannelValues[channel] = channelValue
                            displayLight.changeColourAccordingToFixture()
                if displayLight.lightType == "GenericDimmer":
                    if int(displayLightChannel) == int(channel):
                        self.lightDisplay.universeChannelValues[channel] = channelValue
                        for light in self.lightDisplay.lights:
                            light.updateChannelValuesFromUniverse()
                            light.updateChannelValues()
                        displayLight.changeColourAccordingToFixture()

        self.updateChannels()


    def previousPlaybackButtonClicked(self):
        if self.sequenceID == None:
            self.errorWindow = ErrorWindow("You have not opened a sequence yet so you cannot move to the previous playback.")
        else:
            self.displayingPlaybackID -= 1
            sequenceData = self.dataBaseManager.getAllData("sequence"+str(self.sequenceID))
            if len(sequenceData) == 0:
                self.errorWindow = ErrorWindow("There are no playbacks in this sequence.")
                return
            elif self.displayingPlaybackID == 0:
                self.displayingPlaybackID = len(sequenceData)  #go to the end
            self.openPlayback()


    def removeLight(self,light):
        removed = False
        for l in self.displayLights:
            if light == l:
                removed = True
                l.hide()
                self.displayLights.remove(l)

        if removed == False:
            self.errorWindow = ErrorWindow("Error. light not removed")


    def openButtonClicked(self):
        self.openSequenceWindow = OpenSequenceWindow(self.dataBaseManager,self)
        self.openSequenceWindow.show()

    def openWindowClosed(self):
        self.sequenceName = self.openSequenceWindow.sequence
        self.sequenceID = self.openSequenceWindow.sequenceID
        self.sequenceCreatorID = self.openSequenceWindow.sequenceCreatorID
        self.displayingPlaybackID = 1
        self.setWindowTitle(self.sequenceName)

    def saveSequenceButtonClicked(self):
        saveSequenceWindow = SaveSequenceWindow(self.dataBaseManager,self)
        saveSequenceWindow.show()
        if saveSequenceWindow.errorState != True:
            if saveSequenceWindow.sequenceName != False:
                self.sequenceName = saveSequenceWindow.sequenceName
                self.sequenceID = saveSequenceWindow.newSequenceID
                self.sequenceCreatorID = saveSequenceWindow.newSequenceCreatorID
                self.displayingPlaybackID = 1
                self.setWindowTitle(self.sequenceName)

    def autoSaveSequenceButtonClicked(self):
        saveSequenceWindow = SaveSequenceWindow(self.dataBaseManager,self,True)
        if self.sequenceID and self.sequenceCreatorID and self.sequenceName:
            saveSequenceWindow.newSequenceID = self.sequenceID
            saveSequenceWindow.newSequenceCreatorID = self.sequenceCreatorID
            saveSequenceWindow.sequenceID = self.sequenceID
            saveSequenceWindow.saveSequenceCreator()
            saveSequenceWindow.saveSequence()
        else:
            self.errorWindow = ErrorWindow("You have not saved the sequence yet. Please do this first.")

    def savePlaybackButtonClicked(self):
        if self.sequenceID == None:
            self.errorWindow = ErrorWindow("You have not opened or saved a sequence yet. Please do so before saving a playback")
            return
        else:
            self.playbackWindow = SequencePlaybackWindow(self.dataBaseManager,self)
            self.playbackWindow.show()


    def selectColourButtonClicked(self):
        if self.selectColourButton.isChecked():
            if self.colourSelected:
                self.colourModeSelected = True
            else:
                self.selectColourButton.setChecked(False)
                self.colourModeSelected = False
                self.errorWindow = ErrorWindow("You have not selected a colour yet. Use 'Choose Colour' first.")
        else:
            self.colourModeSelected = False

    def colourPickerButtonClicked(self):
        self.colour = QColorDialog.getColor()
        if self.colour.isValid():
            self.colourSelected = True
        else:
            self.colourSelected = False
            self.errorWindow = ErrorWindow("The colour you have selected is not valid. Please try again")

    def addLightButtonClicked(self):
        self.chooseLightWindow = ChooseLightForSequenceWindow(self)
        self.chooseLightWindow.show()

    def createLight(self,lightType,light,xPos,yPos,openFromSavedSequence=False):
        if lightType == "LEDBar24ChannelMode":
            if openFromSavedSequence:
                channelNumber = light[len(lightType):len(light)]
                for l in self.lights:
                    if int(channelNumber) == int(l.channelNumber):
                        newDisplayLight = SequenceDisplayLight2(self.lightDisplay,self,light,xPos,yPos,lightType)
                        self.displayLights.append(newDisplayLight.box1)
                        self.displayLights.append(newDisplayLight.box2)
                        self.displayLights.append(newDisplayLight.box3)
                        self.displayLights.append(newDisplayLight.box4)
                        self.displayLights.append(newDisplayLight.box5)
                        self.displayLights.append(newDisplayLight.box6)
                        self.displayLights.append(newDisplayLight.box7)
                        self.displayLights.append(newDisplayLight.box8)

            else:
                newDisplayLight = SequenceDisplayLight2(self.lightDisplay,self,light,xPos,yPos,lightType)
                self.displayLights.append(newDisplayLight.box1)
                self.displayLights.append(newDisplayLight.box2)
                self.displayLights.append(newDisplayLight.box3)
                self.displayLights.append(newDisplayLight.box4)
                self.displayLights.append(newDisplayLight.box5)
                self.displayLights.append(newDisplayLight.box6)
                self.displayLights.append(newDisplayLight.box7)
                self.displayLights.append(newDisplayLight.box8)
        elif lightType == "GenericDimmer":
            newDisplayLight = SequenceDisplayLight3(self.lightDisplay,self,light,xPos,yPos,lightType)
            self.displayLights.append(newDisplayLight)
        elif lightType == "Miniscan":
            newDisplayLight = SequenceDisplayLight4(self.lightDisplay,self,light,xPos,yPos,lightType)
            self.displayLights.append(newDisplayLight)

        else:
            newDisplayLight = SequenceDisplayLight(self.lightDisplay,self,light,xPos,yPos,lightType)
            self.displayLights.append(newDisplayLight)

    def mousePressEvent(self,e):
        self.x = e.x()
        self.y = e.y()
        if self.addingLight:
            self.createLight(self.addingLightType,self.addingLight,self.x,self.y)
            self.addingLight = False
        else:
            for light in self.displayLights:
                if self.x > light.xPos-light.clickableLeft and self.x < light.xPos+light.clickableRight:
                    if self.y > light.yPos-light.clickableTop and self.y < light.yPos+light.clickableBottom:
                        if light.lightType == "Miniscan" or light.lightType == "GenericDimmer":
                            channelNumber = int(light.lightName[len(light.lightType):len(light.lightName)])
                            channelValid = False
                            for fixture in self.lightDisplay.lights:
                                if channelNumber == fixture.startChannel:
                                    channelValid = True
                                    self.sliderPannelWindow = SliderPannelWindowSequenceWindow(channelNumber,self.lightDisplay,fixture,light,self)
                                    self.sliderPannelWindow.show()
                            if not channelValid:
                                self.errorWindow = ErrorWindow("Channel Error not valid")
                        else:
                            if self.colourModeSelected:
                                light.changeColour(self.colour)
                            else:
                                self.colour = QColorDialog.getColor()
                                if self.colour.isValid():
                                    light.changeColour(self.colour)
                                else:
                                    self.errorWindow = ErrorWindow("The colour you have selected is not valid. Please try again")
                            self.updateChannels()

    def updateChannels(self):
        self.lightDisplay.universeLock = True
        for light in self.displayLights:
            channelNumber = int(light.lightName[len(light.lightType):len(light.lightName)])
            if light.lightType == "GenericDimmer":
                self.lightDisplay.universeChannelValues[channelNumber] = light.red
            elif light.lightType == "RGBLight" or light.lightType == "RGB6Channel":
                channelNumber += 1   #as the first is intensity
                self.lightDisplay.universeChannelValues[channelNumber] = light.red
                self.lightDisplay.universeChannelValues[channelNumber+1] = light.green
                self.lightDisplay.universeChannelValues[channelNumber+2] = light.blue
            else:
                self.lightDisplay.universeChannelValues[channelNumber] = light.red
                self.lightDisplay.universeChannelValues[channelNumber+1] = light.green
                self.lightDisplay.universeChannelValues[channelNumber+2] = light.blue
        for light in self.lightDisplay.lights:
            light.updateChannelValuesFromUniverse()
            light.updateChannelValues()
        self.lightDisplay.universeLock = False
        self.lightDisplay.universeChanged()
        for light in self.visualLightDisplay.lightList:
            light.changeColourAccordingToFixture()

    def closeEvent(self,e):
        self.visualLightDisplay.isSequenceWindowOpen = False
