from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import math as maths
import time

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

class LightDisplayWindow(QMainWindow,uic.loadUiType("lightDisplayWindow.ui")[0]):  #creates a class window
    def __init__(self,lightDisplay,dataBaseManager):
        self.lightDisplay = lightDisplay
        super(QMainWindow).__init__()     #use super class of QMainWindow
        super(uic.loadUiType("lightDisplayWindow.ui")[0]).__init__()     #use super class of QMainWindow
        super().__init__()     #use super class of QMainWindow
        self.setupUi(self)
        self.setMouseTracking(True)
        self.dataBaseManager = dataBaseManager
        # self.xpos = 0
        # self.width = 1900
        # self.ypos = 0
        # self.height = 1000
        # self.setGeometry(int(self.xpos),int(self.ypos),int(self.width),int(self.height)) #sets window parameters top left is (0,0)
        self.setWindowTitle("Lighting Display") #sets window title
        # self.setStyleSheet("background-color:black")
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

        # self.patchButton = QtWidgets.QPushButton(self)
        # self.patchButton.setText("Patch Light")
        # self.patchButton.setFixedWidth(100)
        # self.patchButton.move(20,10)
        # self.patchButton.setText("Patch Light")
        # self.patchButton.setStyleSheet("color:white;")
        self.patchButton.triggered.connect(self.patchButtonClicked)

        # self.selectButton = QtWidgets.QPushButton(self)
        # self.selectButton.setFixedWidth(100)
        # self.selectButton.move(130,10)
        # self.selectButton.setText("Select Lights")
        # self.selectButton.setStyleSheet("background-color:white")
        # self.selectButton.setCheckable(True)
        self.selectButton.triggered.connect(self.selectButtonClicked)

        # self.effectsButton = QtWidgets.QPushButton(self)
        # self.effectsButton.setFixedWidth(100)
        # self.effectsButton.move(240,10)
        # self.effectsButton.setText("Effects")
        # self.effectsButton.setStyleSheet("background-color:white")
        self.effectsButton.triggered.connect(self.effectsButtonClicked)

        # self.openButton = QtWidgets.QPushButton(self)
        # self.openButton.setFixedWidth(100)
        # self.openButton.move(350,10)
        # self.openButton.setText("Open Rig")
        # self.openButton.setStyleSheet("background-color:white")
        self.openButton.triggered.connect(self.openButtonClicked)

        # self.saveButton = QtWidgets.QPushButton(self)
        # self.saveButton.setFixedWidth(100)
        # self.saveButton.move(460,10)
        # self.saveButton.setText("Save Rig")
        # self.saveButton.setStyleSheet("background-color:white")
        self.saveButton.triggered.connect(self.saveButtonClicked)

        # self.defaultSaveButton = QPushButton(self)
        # self.defaultSaveButton.setFixedWidth(100)
        # self.defaultSaveButton.move(570,10)
        # self.defaultSaveButton.setText("Auto Save")
        # self.defaultSaveButton.setStyleSheet("background-color:white")
        self.defaultSaveButton.triggered.connect(self.defaultSaveButtonClicked)

        # self.recordPlayback = QPushButton(self)
        # self.recordPlayback.setFixedWidth(150)
        # self.recordPlayback.move(680,10)
        # self.recordPlayback.setText("Record Playback")
        # self.recordPlayback.setStyleSheet("background-color:white")
        self.recordPlayback.triggered.connect(self.recordPlaybackClicked)

        # self.playbackButton = QPushButton(self)
        # self.playbackButton.setFixedWidth(100)
        # self.playbackButton.move(840,10)
        # self.playbackButton.setText("Playbacks")
        # self.playbackButton.setStyleSheet("background-color:white")
        self.playbackButton.triggered.connect(self.playbackButtonClicked)

        # self.sequenceButton = QPushButton(self)
        # self.sequenceButton.setFixedWidth(150)
        # self.sequenceButton.move(950,10)
        # self.sequenceButton.setText("Sequence Window")
        # self.sequenceButton.setStyleSheet("background-color:white")
        self.sequenceButton.triggered.connect(self.sequenceButtonClicked)

        # self.openSequenceButton = QPushButton(self)
        # self.openSequenceButton.setFixedWidth(150)
        # self.openSequenceButton.move(1110,10)
        # self.openSequenceButton.setText("Open Sequence")
        # self.openSequenceButton.setStyleSheet("background-color:white")
        self.openSequenceButton.triggered.connect(self.openSequenceButtonClicked)

        # self.snakeButton = QPushButton(self)
        # self.snakeButton.setFixedWidth(100)
        # self.snakeButton.move(1270,10)
        # self.snakeButton.setText("Snake Game")
        # self.snakeButton.setStyleSheet("background-color:white")
        self.snakeButton.triggered.connect(self.snakeButtonClicked)


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
                    confirmWindow = ConfirmWindow(self,playbackOveride = True)
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
                self.dataBaseManager.insertRecord("playback"+str(nextPlaybackID),[None,i,currentChannelValues[i]])
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

    #
    # def mouseMoveEvent(self,e):
    #     print("test")
    #     self.x = e.x()
    #     self.y = e.y()
    #     if self.creatingLight:
    #         print("test")
    #         self.previewLight(self.x,self.y)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if self.creatingLight:
                self.x = event.x()
                self.y = event.y()
                if self.x != 0 and self.y != 0: #gets rid of the random 0's that appear for some reason
                    self.previewLight(self.x,self.y)
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() == Qt.LeftButton:
                self.x = event.x()
                self.y = event.y()
                self.mousePressed(self.x,self.y)
                if self.creatingLight:
                    return 1
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
                            if not channelValid:
                                self.errorWindow = ErrorWindow("Channel Error not valid")
                            return
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
                # selectButton.setStyleSheet("background-color:grey")
            else:
                self.selectingLights = False
                # selectButton.setStyleSheet("background-color:white")

    def effectsButtonClicked(self):
        self.effectsWindow.checkNumberOfLights()
        if len(self.effectsWindow.selectedLights) > 0:
            self.effectsWindow.initialTime = False
            self.effectsWindow.show()
