from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import math as maths
import time
import os

from effectsWindow import EffectsWindow
from snakeWindow import SnakeWindow
from sequenceSelectionWindow import SequenceSelectionWindow
from sequenceWindow import SequenceWindow
from playbackWindow import PlaybackWindow
from errorWindow import ErrorWindow
from patchingWindow import PatchingWindow
from confirmWindow import ConfirmWindow
from saveRigWindow import SaveRigWindow
from openRigWindow import OpenRigWindow
from displayLightTypes import *
from sliderPannelWindow import SliderPannelWindow
from inputPlaybackNameWindow import InputPlaybackNameWindow
from createLightTypeWindow import CreateLightTypeWindow
from lightTypeWindow import LightTypeWindow

class LightDisplayWindow(QMainWindow,uic.loadUiType(os.path.join("ui","lightDisplayWindow.ui"))[0]):  #creates a class window
    def __init__(self,lightDisplay,dataBaseManager):
        self.lightDisplay = lightDisplay
        super(QMainWindow).__init__()     #use super class of QMainWindow
        super(uic.loadUiType(os.path.join("ui","lightDisplayWindow.ui"))[0]).__init__()     #use super class of QMainWindow
        super().__init__()     #use super class of QMainWindow
        self.setupUi(self)
        self.setMouseTracking(True)
        self.dataBaseManager = dataBaseManager
        self.isSequenceWindowOpen = False
        self.setWindowTitle("Lighting Display") #sets window title
        self.creatingLight = False
        self.creatingLightInformation = False
        self.creatingChannel = 0
        self.numberOfLightsToCreate = 0
        self.channelGap = 0
        self.creatingMultipleLights = False
        self.selectingLights = False
        self.lightList = []
        self.tempLight = None
        self.selectedLights = []
        self.effectsWindow = False
        self.rigName = None
        self.rigID = None
        self.creatingDuplicate = False
        self.playbackName = None
        self.runningSequence = False
        self.checkForSpace = False
        self.finishedSequence = False
        self.effectsWindow = EffectsWindow(self.lightDisplay,self.selectedLights,self,True)
        self.initUI()
    def initUI(self):   #create UI
        self.stageLeft = QLabel(self)
        self.stageLeft.move(350,50)
        self.stageLeft.setFixedSize(5,550)
        self.stageLeft.setStyleSheet("background-color:white;")

        self.stageRight = QLabel(self)
        self.stageRight.move(1550,50)
        self.stageRight.setFixedSize(5,550)
        self.stageRight.setStyleSheet("background-color:white;")

        self.stageTop = QLabel(self)
        self.stageTop.move(350,50)
        self.stageTop.setFixedSize(1200,5)
        self.stageTop.setStyleSheet("background-color:white;")

        self.stageBottom = QLabel(self)
        self.stageBottom.move(350,600)
        self.stageBottom.setFixedSize(1200,5)
        self.stageBottom.setStyleSheet("background-color:white;")

        self.createBar("A",900,25,500,700)
        self.createBar("B",900,25,500,900)
        self.createBar("F",900,25,500,500)
        self.createBar("M",900,25,500,300)
        self.createBar("C",900,25,500,100)
        self.createBar("L",25,400,200,570,False)
        self.createBar("L",25,400,1700,570,False)


        self.patchButton.triggered.connect(self.patchButtonClicked)
        self.selectButton.triggered.connect(self.selectButtonClicked)
        self.effectsButton.triggered.connect(self.effectsButtonClicked)
        self.openButton.triggered.connect(self.openButtonClicked)
        self.saveButton.triggered.connect(self.saveButtonClicked)
        self.defaultSaveButton.triggered.connect(self.defaultSaveButtonClicked)
        self.recordPlayback.triggered.connect(self.recordPlaybackClicked)
        self.playbackButton.triggered.connect(self.playbackButtonClicked)
        self.sequenceButton.triggered.connect(self.sequenceButtonClicked)
        self.openSequenceButton.triggered.connect(self.openSequenceButtonClicked)
        self.snakeButton.triggered.connect(self.snakeButtonClicked)
        self.chooseColourButton.triggered.connect(self.chooseColourButtonClicked)
        self.selectAllLightsButton.triggered.connect(self.selectAllLightsButtonClicked)
        self.stopSequenceButton.triggered.connect(self.stopSequenceButtonClicked)
        self.createLightTypeButton.triggered.connect(self.createLightTypeButtonClicked)
        self.selectLightTypeButton.triggered.connect(self.selectLightTypeButtonClicked)


    def createLightTypeButtonClicked(self):
        self.createLightTypeWindow = CreateLightTypeWindow()
        self.createLightTypeWindow.show()


    def stopSequenceButtonClicked(self):
        if self.runningSequence:
            self.sequenceSelectionWindow.loopSequence = False
            self.runningSequence = False
        else:
            self.errorWindow = ErrorWindow("There is no sequence currently running.")

    def selectLightTypeButtonClicked(self):
        if self.selectAllLightsButton.isChecked():
            self.selectAllLightsButtonClicked()
            self.selectAllLightsButton.setChecked(False)
        self.lightTypeWindow = LightTypeWindow(self)
        self.lightTypeWindow.show()

    def selectLightAndDuplicates(self,light):
        light.toggleSelected()
        self.selectedLights.append(light)
        for l in self.lightList: #selects lights of the same channnel
            if l.channelNumber == light.channelNumber and l!=light:
                l.toggleSelected()
                self.selectedLights.append(l)

    def deselectLightAndDuplicates(self,light):
        self.selectedLights.remove(light)
        light.toggleSelected()
        for l in self.lightList:#selects lights of the same channnel
            if l.channelNumber == light.channelNumber and l!=light:
                l.toggleSelected()
                self.selectedLights.remove(l)

    def selectLightsOfType(self,lightType,select=True):
        for light in self.lightList:
            # print(light.lightType)
            if select:
                if not light.selected and light.lightType == lightType:
                    self.selectLightAndDuplicates(light)
            else:
                if light.selected and light.lightType == lightType:
                    self.deselectLightAndDuplicates(light)

    def selectAllLightsButtonClicked(self):
        if not self.selectAllLightsButton.isChecked():
            for light in self.lightList:
                if light.selected:
                    self.deselectLightAndDuplicates(light)
        else:
            if len(self.lightList) == 0:
                self.errorWindow = ErrorWindow("There are no lights to select.")
                self.selectButton.setChecked(False)
                return
            for light in self.lightList:
                if light.selected:
                    pass
                else:
                    self.selectLightAndDuplicates(light)


    def chooseColourButtonClicked(self):
        if len(self.selectedLights) == 0:
            self.errorWindow = ErrorWindow("You have not selected any lights to change the colour for.")
            return
        colour = QColorDialog.getColor()
        if colour.isValid():
            self.setColourToSelectedLights(colour)
        else:
            self.errorWindow = ErrorWindow("The colour you have selected is not valid. Please try again")

    def setColourToSelectedLights(self,colour):
        for l in self.selectedLights:
            valid = False
            for light in self.lightDisplay.lights:
                if light.startChannel == l.channelNumber:
                    valid = True
                    break

            if not valid:
                self.errorWindow("That light does not exist. This is an issue with the code as it should never get here.")
                return
            if l.lightType == "RGBChannel" or l.lightType == "RGB6Channel" or l.lightType == "RGB8Channel" or l.lightType == "RGBWLight":
                for i in range(len(light.channels)):
                    if light.channels[i] == "Red":
                        self.lightDisplay.commitToChannel(i,colour.red(),light.startChannel)
                    elif light.channels[i] == "Green":
                        self.lightDisplay.commitToChannel(i,colour.green(),light.startChannel)
                    elif light.channels[i] == "Blue":
                        self.lightDisplay.commitToChannel(i,colour.blue(),light.startChannel)
                l.changeColourAccordingToFixture()
            elif l.lightType == "LEDBar24ChannelMode":
                for i in range(8):
                    light.channelValues[3*i] = colour.red()
                    light.channelValues[3*i+1] = colour.green()
                    light.channelValues[3*i+2] = colour.blue()
                light.updateChannelValues()
                light.changeUniverse()
                l.changeColourAccordingToFixture()
            elif l.lightType == "GenericDimmer":
                light.channelValues[0] = colour.red()  #as only one channel. This is so we can use this to dim all lights
                light.updateChannelValues()
                light.changeUniverse()
                l.changeColourAccordingToFixture()

    def snakeButtonClicked(self):
        self.snakeWindow = SnakeWindow(self.lightDisplay,self)
        self.snakeWindow.show()

    def openSequenceButtonClicked(self):
        if self.rigID == None:
            self.errorWindow = ErrorWindow("You have not saved or opened a rig. Please do this first.")
            return
        self.sequenceSelectionWindow = SequenceSelectionWindow(self.dataBaseManager,self.lightDisplay,self)
        self.sequenceSelectionWindow.show()

    def sequenceButtonClicked(self):
        if len(self.lightList) < 1:
            self.errorWindow = ErrorWindow("There are no lights to create a sequence with. Try patching one first.")
        elif self.rigID == None:
            self.errorWindow = ErrorWindow("You need to open or save a rig before opening the sequence window.")
        else:
            self.sequenceWindow = SequenceWindow(self.lightDisplay,self,self.dataBaseManager,self.rigID)
            self.isSequenceWindowOpen = True
            self.sequenceWindow.show()

    def playbackButtonClicked(self):
        self.playbackWindow = PlaybackWindow(self,self.dataBaseManager,self.lightDisplay)
        self.playbackWindow.show()

    def recordPlaybackClicked(self):
        if self.rigID == None:
            self.errorWindow = ErrorWindow("You have not opened or saved a rig yet. Please do so before saving a playback")
            return
        nextPlaybackID = self.getNextPlaybackID()
        nameAlreadyUsed = True
        while nameAlreadyUsed:
            inputWindow = InputPlaybackNameWindow("Please Input the name for the playback","Playback Name",self)
            if self.playbackName != None: #playbackname is set by the InputPlaybackNameWindow
                nameAlreadyUsed = self.dataBaseManager.checkIfPlaybackNameExistsInRig(self.rigID,self.playbackName)
                if nameAlreadyUsed:
                    self.removeConfirmed = False
                    confirmWindow = ConfirmWindow(self,"This name already exisists. Do you want to overide it.")
                    if not self.removeConfirmed:
                        return
                    else:
                        self.dataBaseManager.dropPlaybackTable(self.rigID,self.playbackName)
                        self.dataBaseManager.deletePlaybackFromPlaybacksTable(self.rigID,self.playbackName)
                        break
            else:
                return  #as window closed without pressing OK
        self.dataBaseManager.createPlaybackTable(nextPlaybackID)
        self.dataBaseManager.insertRecord("Playbacks",[None,nextPlaybackID,self.rigID,self.playbackName])
        #possbly needs universe lock here
        currentChannelValues = self.lightDisplay.universeChannelValues
        for i in range(len(currentChannelValues)):
            if self.lightDisplay.channelsOccupied[i] == 1:
                self.dataBaseManager.insertRecord("playback"+str(nextPlaybackID),[None,i+1,currentChannelValues[i+1]])
        if self.lightDisplay.runningRainbow:
            rainbowValue = self.effectsWindow.rainbowDelay
        else:
            rainbowValue = False
        if self.lightDisplay.runningChaser:
            chaserValue = self.effectsWindow.chaserDelay
        else:
            chaserValue = False
        self.dataBaseManager.insertRecord("playback"+str(nextPlaybackID),[None,"rainbow",rainbowValue])
        self.dataBaseManager.insertRecord("playback"+str(nextPlaybackID),[None,"chaser",chaserValue])  #add other effects when created here
        for i in range(len(self.selectedLights)):
            self.dataBaseManager.insertRecord("playback"+str(nextPlaybackID),[None,"SelectedLight",str(self.selectedLights[i].channelNumber)])
        self.playbackName = None  #reset to none for next time

    def getNextPlaybackID(self):
        exisits = True
        counter = 0
        while exisits:
            exisits = self.dataBaseManager.checkIfTableExisits("playback"+str(counter))
            counter += 1
        counter -= 1 #as the last one didn't exist so this is the next one
        return counter

    def defaultSaveButtonClicked(self):
        saveRigWindow = SaveRigWindow(self.dataBaseManager,self.lightDisplay,self,True)
        if self.rigName and self.rigID:
            saveRigWindow.rigName = self.rigName
            saveRigWindow.newRigID = self.rigID
            saveRigWindow.saveRig()
        else:
            self.errorWindow = ErrorWindow("You have not saved or opened a rig so you cannot auto save it yet.")

    def openButtonClicked(self):
        self.openRigWindow = OpenRigWindow(self.dataBaseManager,self.lightDisplay,self)
        self.openRigWindow.show()

    def openWindowClosed(self):
        self.rigName = self.openRigWindow.rig
        self.rigID = self.openRigWindow.rigID
        self.setWindowTitle(self.rigName)

    def saveButtonClicked(self):
        saveRigWindow = SaveRigWindow(self.dataBaseManager,self.lightDisplay,self)
        saveRigWindow.show()
        if saveRigWindow.errorState != True and saveRigWindow.rigName != False:
            self.rigName = saveRigWindow.rigName
            self.rigID = saveRigWindow.newRigID
            self.setWindowTitle(saveRigWindow.rigName)

    def createLight(self,xPos,yPos,channel):
        if self.tempLight:
            self.tempLight.hide()
        if self.lightInformation.lightType == "LEDBar24ChannelMode":
            self.newLight = DisplayLight2(self.tempLight.xPos,self.tempLight.yPos,channel,self.lightDisplay,self)
        elif self.lightInformation.lightType == "GenericDimmer":
            self.newLight = DisplayLight3(self.tempLight.xPos,self.tempLight.yPos,channel,self.lightDisplay,self)
        elif self.lightInformation.lightType == "Miniscan":
            self.newLight = DisplayLight4(self.tempLight.xPos,self.tempLight.yPos,channel,self.lightDisplay,self)
        else:
            self.newLight = DisplayLight(self.tempLight.xPos,self.tempLight.yPos,channel,self.lightDisplay,self)
        self.newLight.lightType = self.lightInformation.lightType
        self.lightList.append(self.newLight)

    def createLightFromSavedRig(self,light,xpos,ypos,lightType,channel):
        if lightType == "LEDBar24ChannelMode":
            self.newLight = DisplayLight2(xpos,ypos,channel,self.lightDisplay,self)
        elif lightType == "GenericDimmer":
            self.newLight = DisplayLight3(xpos,ypos,channel,self.lightDisplay,self)
        elif lightType == "Miniscan":
            self.newLight = DisplayLight4(xpos,ypos,channel,self.lightDisplay,self)
        else:
            self.newLight = DisplayLight(xpos,ypos,channel,self.lightDisplay,self)
        self.newLight.lightType = lightType
        self.lightList.append(self.newLight)

    def previewLight(self,xPos,yPos):
        if self.tempLight:
            self.tempLight.hide()
        channel = None
        if self.lightInformation.lightType == "LEDBar24ChannelMode":
            self.tempLight = DisplayLight2(xPos,yPos,channel,self.lightDisplay,self)
        elif self.lightInformation.lightType == "GenericDimmer":
            self.tempLight = DisplayLight3(xPos,yPos,channel,self.lightDisplay,self)
        elif self.lightInformation.lightType == "Miniscan":
            self.tempLight = DisplayLight4(xPos,yPos,channel,self.lightDisplay,self)

        else:
            self.tempLight = DisplayLight(xPos,yPos,channel,self.lightDisplay,self)

    def eventFilter(self, source, event):
        if not self.isSequenceWindowOpen:
            if self.creatingLight:
                if event.type() == QEvent.MouseMove:
                    self.x = event.x()
                    self.y = event.y()
                    if self.x != 0 and self.y != 0: #gets rid of the random 0's that appear for some reason
                        self.previewLight(self.x,self.y)
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() == Qt.LeftButton:
                    self.x = event.x()
                    self.y = event.y()
                    returnNormal = self.mousePressed(self.x,self.y)
                    if self.creatingLight:
                        return 1
                    if returnNormal is None:
                        pass
                    else:
                        return 1
            if (event.type() == QEvent.KeyPress):
                key = event.key()
                if key == Qt.Key_Space:
                    if self.checkForSpace == True:
                        self.checkForSpace = False
                        self.sequenceSelectionWindow.openIndividualSequence()
                        return 1 #needed to stop double trigger

        return super(LightDisplayWindow, self).eventFilter(source, event)


    def mousePressed(self,x,y,resetMode = False):
        if not resetMode:
            self.x = x
            self.y = y
            if self.selectingLights:
                lightClicked = False
                for light in self.lightList:
                    if self.x > light.xPos-light.clickableLeft and self.x < light.xPos+light.clickableRight:
                        if self.y > light.yPos-light.clickableTop and self.y < light.yPos+light.clickableBottom:
                            lightClicked = True
                            light.toggleSelected()
                            if light.selected:
                                self.selectedLights.append(light)
                                for l in self.lightList:
                                    if l.channelNumber == light.channelNumber and l!=light:
                                        l.toggleSelected()
                                        self.selectedLights.append(l)
                            else:
                                self.selectedLights.remove(light)
                                for l in self.lightList:
                                    if l.channelNumber == light.channelNumber and l!=light:
                                        l.toggleSelected()
                                        self.selectedLights.remove(l)
                if not lightClicked:
                    if self.creatingLight:
                        if self.creatingMultipleLights:
                            channelToCreateLightWith = self.creatingLightChannel-((self.numberOfLightsToCreate-1)*len(self.creatingLightInformation.channels)) - (self.channelGap*(self.numberOfLightsToCreate-1))
                        else:
                            channelToCreateLightWith = self.creatingLightChannel
                        self.createLight(self.x,self.y,channelToCreateLightWith)  #if error then change me back?
                        try:
                            self.createLight(self.x,self.y,channelToCreateLightWith)
                        except:
                            self.errorWindow = ErrorWindow("Error with creating light. Possibly type of light error?")
                        self.numberOfLightsToCreate -= 1
                        if self.numberOfLightsToCreate == 0:
                            self.creatingLight = False
            else:
                lightClicked = False
                for light in self.lightList:
                    if self.x > light.xPos-light.clickableLeft and self.x < light.xPos+light.clickableRight:
                        if self.y > light.yPos-light.clickableTop and self.y < light.yPos+light.clickableBottom:
                            lightClicked = True
                            channelValid = False
                            for fixture in self.lightDisplay.lights:
                                if light.channelNumber == fixture.startChannel:
                                    channelValid = True
                                    self.sliderPannelWindow = SliderPannelWindow(light.channelNumber,self.lightDisplay,fixture,light,self)
                                    self.sliderPannelWindow.show()
                                    return False
                            if not channelValid:
                                self.errorWindow = ErrorWindow("Channel Error not valid")
                if not lightClicked:
                    if self.creatingLight:
                        if self.creatingMultipleLights:
                            channelToCreateLightWith = self.creatingLightChannel-((self.numberOfLightsToCreate-1)*len(self.creatingLightInformation.channels)) - (self.channelGap*(self.numberOfLightsToCreate-1))
                        else:
                            channelToCreateLightWith = self.creatingLightChannel
                        try:
                            self.createLight(self.x,self.y,channelToCreateLightWith)
                        except:
                            self.errorWindow = ErrorWindow("Error with creating light. Possibly type of light error?")
                        self.numberOfLightsToCreate -= 1
                        if self.numberOfLightsToCreate == 0:
                            self.creatingLight = False
                        return

    def removeLight(self,light):
        removed = False
        for l in self.lightList:
            if light == l:
                removed = True
                l.hide()
                for i in range(len(self.selectedLights)):
                    if light == self.selectedLights[i]:
                        light.toggleSelected()
                self.lightList.remove(l)

        if removed == False:
            self.errorWindow = ErrorWindow("Error. light not removed")

    def createBar(self,barName,width,height,xPos,yPos,horizontal = True):
        self.a = QLabel(self)
        self.a.move(xPos,yPos)
        self.a.setFixedSize(width,height)
        self.a.setStyleSheet("background-color:white; border: 1px solid white;")
        if horizontal:
            self.createBarLabel(barName,xPos+width+50,yPos-15)
        else: #so vertical
            self.createBarLabel(barName,xPos-15,yPos-75)

    def createBarLabel(self,barName,xPos,yPos):
        self.barLabel = QLabel(self)
        self.barLabel.move(int(xPos),int(yPos))
        self.barLabel.setFixedSize(50,50)
        self.barLabel.setStyleSheet("background-color:white; border: 1px solid white;font-size: 30px;")
        self.barLabel.setText(barName)
        self.barLabel.setAlignment(Qt.AlignCenter)

    def patchButtonClicked(self):
        self.patchPannel = PatchingWindow(self.lightDisplay,self)
        self.patchPannel.show()

    def selectButtonClicked(self):
        if self.sender() != None:
            selectButton = self.sender()
            if selectButton.isChecked():
                self.selectingLights = True
            else:
                self.selectingLights = False

    def effectsButtonClicked(self):
        self.effectsWindow.checkNumberOfLights()
        if len(self.effectsWindow.selectedLights) > 0:
            self.effectsWindow.initialTime = False
            self.effectsWindow.show()

    def closeEvent(self,e):
        try:
            self.lightDisplay.sendzero()
        except:
            pass #as this will be in test mode so dmx is not connected
