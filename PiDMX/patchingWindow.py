from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from errorWindow import ErrorWindow

class PatchingWindow(QWidget):
    def __init__(self,lightDisplay,displayWindow = False):
        super().__init__()
        xpos = 200
        ypos = 200
        width = 1050
        height = 750
        self.displayWindow = displayWindow
        self.lightDisplay = lightDisplay
        self.setGeometry(int(xpos),int(ypos),int(width),int(height)) #sets window parameters top left is (0,0)
        self.setWindowTitle("Light Patching") #sets window title
        self.initUI()
    def initUI(self):
        self.startChannelBox = QLineEdit(self)
        self.startChannelBox.setPlaceholderText("Enter Start Channel")
        self.startChannelBox.move(50,50)

        self.lightType = QComboBox(self) #drop down menu
        for light in self.lightDisplay.lightsInformation:
            self.lightType.addItem(light.dropdownName)
        self.lightType.move(250,50)

        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.move(50,250)
        self.submitButton.setText("Submit")
        self.submitButton.clicked.connect(self.submitButtonPressed)

        self.radio1 = QRadioButton(self)
        self.radio1.move(50,100)
        self.radio1.setText("Patch One Light")
        self.radio1.setChecked(True)


        self.radio2 = QRadioButton(self)
        self.radio2.move(50,120)
        self.radio2.setText("Patch Multiple Lights")


        self.numberOfFixturesBox = QLineEdit(self)
        self.numberOfFixturesBox.setPlaceholderText("Enter number of fixtures")
        self.numberOfFixturesBox.move(50,150)

        self.channelGap = QLineEdit(self)
        self.channelGap.setPlaceholderText("Enter the channel gap")
        self.channelGap.move(50,180)

        self.labelList = []
        startXPos = 15
        startYPos = 400
        xGap = 32  #change back to 24
        yGap = 20
        noX = 32
        noY = 16
        xCoords = []
        yCoords = []
        for i in range(noX):
            xCoords.append(startXPos+xGap*i)
        for i in range(noY):
            yCoords.append(startYPos+yGap*i)


        for i in range(noX):
            for j in range(noY):
                self.newLabel = self.createLabelForGrid(xCoords[i],yCoords[j],j*noX+i+1)  #+1 as counting from 1 not 0
                self.labelList.append(self.newLabel)

    def createLabelForGrid(self,moveX,moveY,number):
        self.newLabel = QtWidgets.QLabel(self)
        self.newLabel.setText(str(number))
        self.newLabel.setFixedWidth(30)   #change back to 22
        self.newLabel.move(moveX,moveY)
        if self.lightDisplay.channelsOccupied[number-1] == 0:  #-1 as number dosen't count from 0 but the list does
            self.newLabel.setStyleSheet("background-color: lightgrey;color: black; border: 2px solid green;")
        elif self.lightDisplay.channelsOccupied[number-1] == 1:
            self.newLabel.setStyleSheet("background-color: lightgrey;color: black; border: 2px solid red;")

        self.newLabel.setAlignment(Qt.AlignCenter)


    def submitButtonPressed(self):
        if self.radio1.isChecked():
            self.patchSingleLight()
        elif self.radio2.isChecked():
            self.patchMultipleLights()


    def patchSingleLight(self):
        channel = self.startChannelBox.text()
        isInteger = self.checkIfInteger(channel)
        if isInteger:
            channel = int(channel)
            isInRange = self.checkIfChannelInRange(channel)
            if isInRange:
                lightInformation = self.getLightInformation()
                amountOfChannels = len(lightInformation.channelValues)
                startChannel = channel
                endChannel = int(channel + amountOfChannels)
                isNotOverlapping = self.checkIfChannelsOverlapping(startChannel,endChannel)
                if isNotOverlapping:
                    self.newLight = lightInformation.generateNewLight(channel)
                    self.newLight.lightDisplay = self.lightDisplay
                    self.newLight.changeUniverse()
                    self.lightDisplay.lights.append(self.newLight)
                    self.lightDisplay.updateOccupiedChannels()
                    if self.displayWindow:
                        self.displayOnWindow(self.newLight,lightInformation,False)
                    self.close()

    def patchMultipleLights(self):
        channel = self.startChannelBox.text()
        isInteger = self.checkIfInteger(channel)
        if isInteger:
            channel = int(channel)
            channelGap = self.channelGap.text()
            isIntegerChannelGap = self.checkIfInteger(channelGap)
            if isIntegerChannelGap:
                channelGap = int(channelGap)
                numberOfFixtures = self.numberOfFixturesBox.text()
                isInRange = self.checkIfChannelInRange(channel)
                if isInRange:
                    lightInformation = self.getLightInformation()
                    amountOfChannels = len(lightInformation.channelValues)
                    isIntegerNoFixtures = self.checkIfInteger(numberOfFixtures)
                    valid = True
                    if isIntegerNoFixtures:
                        numberOfFixtures = int(numberOfFixtures)
                        for i in range(numberOfFixtures):
                            startChannel = channel + i*(amountOfChannels+channelGap)
                            endChannel = startChannel + amountOfChannels -1
                            isNotOverlapping = self.checkIfChannelsOverlapping(startChannel,endChannel)
                            if not isNotOverlapping:
                                valid = False
                                break
                        if valid:
                            for i in range(numberOfFixtures):
                                self.newLight = lightInformation.generateNewLight(channel+i*(amountOfChannels+channelGap))
                                self.newLight.lightDisplay = self.lightDisplay
                                self.newLight.changeUniverse()
                                self.lightDisplay.lights.append(self.newLight)
                                self.lightDisplay.updateOccupiedChannels()
                                if self.displayWindow:
                                    self.displayOnWindow(self.newLight,lightInformation,True)
                            self.close()


    def displayOnWindow(self,light,lightInformation,patchingMultipleLights = False):
        self.displayWindow.numberOfLightsToCreate += 1
        if patchingMultipleLights:
            self.displayWindow.channelGap = int(self.channelGap.text())
            self.displayWindow.creatingLightInformation = lightInformation
            self.displayWindow.creatingMultipleLights = True
        else:
            self.displayWindow.creatingMultipleLights = False

        self.displayWindow.creatingLight = True
        self.displayWindow.creatingLightChannel = light.startChannel
        self.displayWindow.lightInformation = lightInformation


    def checkIfChannelsOverlapping(self,startChannel,endChannel):
        for i in range(endChannel-startChannel):
            if startChannel + i >= len(self.lightDisplay.channelsOccupied):
                self.errorWindow = ErrorWindow("The lights you have tried to patch are out of range. Please try again.")
                return False
            if self.lightDisplay.channelsOccupied[startChannel+i-1] == 1: #startChannel+i-1 as list starts from 0
                self.errorWindow = ErrorWindow("Some or all of the channels overlap with existing fixtures. Please try again.")
                return False
        return True



    def checkIfChannelInRange(self,channel):
        if channel > 512 or channel < 1:
            self.errorWindow = ErrorWindow("The channel you have entered is out of range. Please try again")
            return False
        else:
            return True

    def getLightInformation(self):
        for light in self.lightDisplay.lightsInformation:
            if light.dropdownName == self.lightType.currentText():
                return light
        self.errorWindow = ErrorWindow("Something went wrong with choosing the light.")
        return False

    def checkIfInteger(self,channel):
        try:
            channel = int(channel)
            return True
        except:
            self.errorWindow = ErrorWindow("The channel you have entered is not valid. Please try again")
            return False
