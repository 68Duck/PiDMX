from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import math as maths

from confirmWindow import ConfirmWindow
from errorWindow import ErrorWindow
from panTiltGridWindow import PanTiltGridWindow
from messageWindow import MessageWindow


class SliderPannelWindow(QWidget):  #creates a class window
    def __init__(self,channelNumber,lightDisplay,light,displayWindowLight = False,displayWindow = False,sequenceWindowMode = False):
        super().__init__()     #use super class of QMainWindow
        self.displayWindowLight = displayWindowLight
        self.sequenceWindowMode = sequenceWindowMode
        self.displayWindow = displayWindow
        self.channel = channelNumber
        self.lightDisplay = lightDisplay
        self.light = light
        if len(self.light.channels) > 12:
            height = 900
            ypos = 100
            xpos = 10
            width = 100+150*12
        else:
            xpos = 10
            ypos = 100
            height = 500
            width = max(100+(len(self.light.channels))*150,800)
        # width = 800
        self.copyValue = None
        self.colourMode = False
        self.setGeometry(int(xpos),int(ypos),int(width),int(height)) #sets window parameters top left is (0,0)
        self.setWindowTitle("Slider Pannel for channel {}".format(self.channel)) #sets window title
        self.initUI()
    def initUI(self):   #create UI
        self.sliders = []
        self.textBoxes = []
        self.slidersSelected = []
        self.selectButtonList = []

        self.colourButton = QPushButton(self)
        self.colourButton.setFixedWidth(100)
        self.colourButton.move(20,10)
        self.colourButton.setText("Select Colour")
        self.colourButton.setStyleSheet("background-color:lightgrey")
        self.colourButton.clicked.connect(self.colourButtonClicked)

        self.selectAllButton = QPushButton(self)
        self.selectAllButton.setFixedWidth(100)
        self.selectAllButton.move(120,10)
        self.selectAllButton.setText("Select All")
        self.selectAllButton.setCheckable(True)
        self.selectAllButton.setStyleSheet("background-color:lightgrey")
        self.selectAllButton.clicked.connect(self.selectAllSelectButtons)


        for i in range(len(self.light.channels)):

            yValue = 50+400*maths.floor(i/12)  #12 as this fits on the screen
            self.createSliderAndTextBoxAndLabel(100+(i%12)*150,yValue,"Enter "+str(self.light.channels[i]),0,255,True,str(self.light.channels[i]),self.light.returnChannelValues()[i],i)


        self.sliderChangedValue()
        panTilt = False
        if type(self.light).__name__ == "LightFromDatabase":
            if self.light.lightInformation["hasPanTilt"] == "1":
                panTilt = True

        if self.light.lightType == "Miniscan" or panTilt:
            self.panTiltGridButton = QPushButton(self)
            self.panTiltGridButton.setFixedWidth(150)
            self.panTiltGridButton.move(520,10)
            self.panTiltGridButton.setText("Pan/tilt grid")
            self.panTiltGridButton.setStyleSheet("background-color:lightgrey")
            self.panTiltGridButton.clicked.connect(self.panTiltGridButtonClicked)

        if self.displayWindowLight:
            self.removeFixtureButton = QPushButton(self)
            self.removeFixtureButton.setFixedWidth(150)
            self.removeFixtureButton.move(220,10)
            self.removeFixtureButton.setText("Remove fixture")
            self.removeFixtureButton.setStyleSheet("background-color:lightgrey")
            self.removeFixtureButton.clicked.connect(self.removeFixtureButtonClicked)

            self.duplicateFixtureButton = QPushButton(self)
            self.duplicateFixtureButton.setFixedWidth(150)
            self.duplicateFixtureButton.move(370,10)
            self.duplicateFixtureButton.setText("Duplicate fixture")
            self.duplicateFixtureButton.setStyleSheet("background-color:lightgrey")
            self.duplicateFixtureButton.clicked.connect(self.duplicateFixtureButtonClicked)

            self.moveFixtureButton = QPushButton(self)
            self.moveFixtureButton.setFixedWidth(150)
            self.moveFixtureButton.move(670 if self.light.lightType == "Miniscan" or panTilt else 520 ,10)
            self.moveFixtureButton.setText("Move fixture")
            self.moveFixtureButton.setStyleSheet("background-color:lightgrey")
            self.moveFixtureButton.clicked.connect(self.moveFixtureButtonClicked)

        if self.light.lightType == "LEDBar24ChannelMode":
            self.invertButton = QPushButton(self)
            self.invertButton.setFixedWidth(150)
            self.invertButton.move(520 ,10)
            self.invertButton.setText("Invert fixture")
            self.invertButton.setStyleSheet("background-color:lightgrey")
            self.invertButton.clicked.connect(self.invertButtonClicked)

    def invertButtonClicked(self):
        self.light.invert()
        self.messageWindow = MessageWindow("The light was inverted so the channels will convert the channels in the opposite order")

    def moveFixtureButtonClicked(self): #create duplicate and then remove the current light
        self.displayWindow.numberOfLightsToCreate += 1
        self.displayWindow.creatingLight = True
        self.displayWindow.creatingMultipleLights = False  #as creating one duplicate
        self.displayWindow.creatingLightChannel = self.light.startChannel
        for light in self.lightDisplay.lightsInformation:
            if self.light.lightType == light.lightType:
                self.displayWindow.lightInformation = light
        self.displayWindow.creatingLightChannel = self.light.startChannel


        self.displayWindow.removeLight(self.displayWindowLight)
        self.hide()

    def panTiltGridButtonClicked(self):
        self.panTiltGrid = PanTiltGridWindow(self)
        self.panTiltGrid.show()

    def createSliderAndTextBoxAndLabel(self,startX,startY,textMessage,minVal,maxVal,isVertical,labelText,sliderStartValue,sliderNumber):
        if isVertical:
            self.newSlider = QSlider(Qt.Vertical,self)
            self.newSlider.setMaximum(maxVal)
            self.newSlider.setMinimum(minVal)
            self.newSlider.setValue(int(sliderStartValue))
            self.newSlider.setGeometry(30,40,30,200)
            self.newSlider.move(startX,startY)
            self.newSlider.valueChanged[int].connect(self.sliderChangedValue)
            self.newSlider.sliderNumber = sliderNumber
            self.newSlider.message = textMessage#for finding pan/tilt in pan/tilt grid
            self.sliders.append(self.newSlider)

            self.newTextBox = QLineEdit(self)
            self.newTextBox.move((startX-35),(startY+350))
            self.newTextBox.setPlaceholderText(textMessage) #sets the message of the text box before any text is entered
            self.newTextBox.setAlignment(Qt.AlignCenter)
            self.newTextBox.textEdited.connect(self.textBoxChangedValue)
            self.newTextBox.setFixedWidth(100)
            self.newTextBox.setText(str(sliderStartValue))
            self.newTextBox.sliderNumber = sliderNumber
            self.textBoxes.append(self.newTextBox)

            self.newLabel = QtWidgets.QLabel(self) #creates label on window. as self is the window
            self.newLabel.setText(labelText) #sets label text
            self.newLabel.setFixedWidth(100)
            self.newLabel.move(startX-35,startY+250)
            self.newLabel.setAlignment(Qt.AlignCenter)

            self.copyButton = QPushButton(self)
            self.copyButton.setText("Copy")
            self.copyButton.setFixedWidth(100)
            self.copyButton.move(startX-35,startY+275)
            self.copyButton.clicked.connect(self.copySliderValue)
            self.copyButton.sliderNumber = sliderNumber
            self.copyButton.setStyleSheet("background-color:lightgrey")

            self.pasteButton = QPushButton(self)
            self.pasteButton.setText("Paste")
            self.pasteButton.setFixedWidth(100)
            self.pasteButton.move(startX-35,startY+300)
            self.pasteButton.clicked.connect(self.pasteToSlider)
            self.pasteButton.sliderNumber = sliderNumber
            self.pasteButton.setStyleSheet("background-color:lightgrey")

            self.selectButton = QPushButton("Toggle",self)
            self.selectButton.setText("Select")
            self.selectButton.setFixedWidth(100)
            self.selectButton.move(startX-35,startY+200)
            self.selectButton.clicked.connect(self.selectButtonPressed)
            self.selectButton.sliderNumber = sliderNumber
            self.selectButton.setCheckable(True)
            self.selectButton.setStyleSheet("background-color:lightgrey")
            self.selectButtonList.append(self.selectButton)

        else:
            print("THIS FEATURE DOSENT EXIST")

    def removeFixtureButtonClicked(self):
        confirmWindow = ConfirmWindow(self,"Are you sure you want to remove this light?")
        if self.removeConfirmed == True:

            numberOfSameLight = 0
            for light in self.displayWindow.lightList:
                if light.channelNumber == self.light.startChannel:
                    numberOfSameLight += 1
            if numberOfSameLight > 1:  #so there are duplicate fixtures
                pass
            else:  #only set the channelValues to 0 and remove the light if it is the last one present
                for i in range(len(self.light.channelValues)):
                    self.light.channelValues[i] = 0
                self.lightDisplay.lights.remove(self.light)
                self.lightDisplay.updateOccupiedChannels()
                self.light.changeUniverse()
            self.displayWindow.removeLight(self.displayWindowLight)
            self.hide()

    def duplicateFixtureButtonClicked(self):
        self.displayWindow.numberOfLightsToCreate += 1
        self.displayWindow.creatingLight = True
        self.displayWindow.creatingMultipleLights = False  #as creating one duplicate
        self.displayWindow.creatingLightChannel = self.light.startChannel
        for light in self.lightDisplay.lightsInformation:
            if self.light.lightType == light.lightType:
                self.displayWindow.lightInformation = light
        self.displayWindow.creatingLightChannel = self.light.startChannel
        self.hide()

    def selectButtonPressed(self):
        selectButton = self.sender()
        if selectButton.isChecked():
            selectButton.setStyleSheet("background-color:lightblue")
            self.slidersSelected.append(selectButton.sliderNumber)
        else:
            selectButton.setStyleSheet("background-color:lightgrey")
            self.slidersSelected.remove(selectButton.sliderNumber)

    def selectAllSelectButtons(self):
        selectAllButton = self.sender()
        if selectAllButton.isChecked():
            selectAllButton.setStyleSheet("background-color:lightblue")
            for selectButton in self.selectButtonList:
                self.autoSelectButton(selectButton)
        else:
            selectAllButton.setStyleSheet("background-color:lightgrey")
            for selectButton in self.selectButtonList:
                self.autoDeselectButton(selectButton)

    def autoDeselectButton(self,selectButton):
        if selectButton.isChecked():
            selectButton.toggle()
            selectButton.setStyleSheet("background-color:lightgrey")
            self.slidersSelected.remove(selectButton.sliderNumber)
        else:
            pass

    def autoSelectButton(self,selectButton):
        if selectButton.isChecked():
            pass
        else:
            selectButton.toggle()
            selectButton.setStyleSheet("background-color:lightblue")
            self.slidersSelected.append(selectButton.sliderNumber)



    def copySliderValue(self):
        copyButton = self.sender()   #gets the copy button that was pressed
        self.copyValue = self.sliders[copyButton.sliderNumber].value()

    def pasteToSlider(self):
        pasteButton = self.sender()
        if self.copyValue == None:
            self.errorWindow = ErrorWindow("You have not coppied a value yet. Please try again")
        else:
            self.sliders[pasteButton.sliderNumber].setValue(int(self.copyValue))
            self.sliderChangedValue(False)


    def sliderChangedValue(self,checkForSelected = True):
        if checkForSelected and not self.colourMode:
            changedSlider = self.sender()
            isSelected = False
            for i in range(len(self.slidersSelected)):
                if changedSlider.sliderNumber == self.slidersSelected[i]:
                    isSelected = True
            if isSelected:
                for slider in self.slidersSelected:
                    self.sliders[slider].setValue(int(changedSlider.value()))

        if not self.sequenceWindowMode:
            for i in range(len(self.textBoxes)):   ##sliders and textboxes should be the same length
                self.textBoxes[i].setText(str(self.sliders[i].value()))

            if self.displayWindowLight:
                for light in self.displayWindow.lightList:
                    finished = light.changeColourAccordingToFixture()

        self.updateChannelValues()  #remove me to stop sending data after each slider is moved if becomes too slow


    def textBoxChangedValue(self):
        if not self.colourMode:
            changedTextBox = self.sender()
            isSelected = False
            for i in range(len(self.slidersSelected)):
                if changedTextBox.sliderNumber == self.slidersSelected[i]:
                    isSelected = True
            if isSelected:
                for slider in self.slidersSelected:  #textboxes and sliders should have the same number
                    self.textBoxes[slider].setText(str(changedTextBox.text()))

        overallValid = True
        for i in range(len(self.textBoxes)):   ##sliders and textboxes should be the same length
            try:
                self.sliders[i].setValue(int(self.textBoxes[i].text()))
                currentValid = True
            except:
                self.textBoxes[i].setText(str(""))
                currentValid = False
                overAllValid = False
            if currentValid:
                if int(self.textBoxes[i].text())>255:
                    self.textBoxes[i].setText(str(255))
                elif int(self.textBoxes[i].text())<0:
                    self.textBoxes[i].setText(str(0))

        if not self.sequenceWindowMode:
            if self.displayWindowLight:
                for light in self.displayWindow.lightList:
                    finished = light.changeColourAccordingToFixture()


    def colourButtonClicked(self):
        self.colourMode = True
        colour = QColorDialog.getColor()
        if colour.isValid():

            if self.light.lightType == "RGBLight" or self.light.lightType == "RGB6Channel" or self.light.lightType == "RGB8Channel" or self.light.lightType == "RGBWLight":
                for i in range(len(self.light.channels)):
                    if self.light.channels[i] == "Red":
                        self.sliders[i].setValue(colour.red())
                    if self.light.channels[i] == "Green":
                        self.sliders[i].setValue(colour.green())
                    if self.light.channels[i] == "Blue":
                        self.sliders[i].setValue(colour.blue())
                self.sliderChangedValue(False)
                self.updateChannelValues()


            elif len(self.slidersSelected)% 3 == 0 and len(self.slidersSelected)>0:
                self.slidersSelected.sort()
                for i in range(len(self.slidersSelected)//3):
                    self.sliders[self.slidersSelected[i*3]].setValue(colour.red())
                    self.sliders[self.slidersSelected[i*3+1]].setValue(colour.green())
                    self.sliders[self.slidersSelected[i*3+2]].setValue(colour.blue())
                self.sliderChangedValue(False)
                self.updateChannelValues()

            elif self.light.lightType == "LEDBar24ChannelMode":
                for i in range(8):
                    self.sliders[i*3].setValue(colour.red())
                    self.sliders[i*3+1].setValue(colour.green())
                    self.sliders[i*3+2].setValue(colour.blue())
                self.sliderChangedValue(False)
                self.updateChannelValues()

            else:
                databaseLight = False
                if type(self.light).__name__ == "LightFromDatabase":
                    databaseLight = True
                if databaseLight:
                    if self.light.lightInformation["isRGB"] == "1":
                        channelInformation = self.light.lightInformation["channelInformation"]
                        for channel in channelInformation:
                            if channel["channelInformation"] is not None:
                                if channel["channelInformation"] == "red":
                                    redChannelName = channel["channelName"]
                                if channel["channelInformation"] == "green":
                                    greenChannelName = channel["channelName"]
                                if channel["channelInformation"] == "blue":
                                    blueChannelName = channel["channelName"]
                        for i in range(len(self.light.channels)):
                            if self.light.channels[i] == redChannelName:
                                self.sliders[i].setValue(colour.red())
                            if self.light.channels[i] == greenChannelName:
                                self.sliders[i].setValue(colour.green())
                            if self.light.channels[i] == blueChannelName:
                                self.sliders[i].setValue(colour.blue())
                        self.sliderChangedValue(False)
                        self.updateChannelValues()
                    else:
                        self.errorWindow = ErrorWindow("There is nowhere to put the colour. Try selecting 3 channels to select the colour of.")
                else:
                    self.errorWindow = ErrorWindow("There is nowhere to put the colour. Try selecting 3 channels to select the colour of.")

        else:
            self.errorWindow = ErrorWindow("The colour you have selected is not valid. Please try again")
        self.colourMode = False

    def updateChannelValues(self):
        for i in range(len(self.sliders)-1):
            self.lightDisplay.commitToChannel(i,self.sliders[i].value(),self.channel,True)
        self.lightDisplay.commitToChannel(len(self.sliders)-1,self.sliders[len(self.sliders)-1].value(),self.channel)

        if self.sequenceWindowMode:
            self.displayWindowLight.changeColourAccordingToFixture()
        else:
            if self.displayWindowLight:
                for light in self.displayWindow.lightList:
                    finished = light.changeColourAccordingToFixture()

    def closeEvent(self,e):
        self.updateChannelValues()
