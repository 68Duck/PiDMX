from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from errorWindow import ErrorWindow

class EffectsWindow(QWidget):
    def __init__(self,lightDisplay,selectedLights,visualLightDisplay,initialTime = False):
        super().__init__()
        xpos = 200
        ypos = 200
        width = 1050
        height = 750
        self.initialTime = initialTime
        self.maxTimeDelayChaser = 2
        self.minTimeDelayChaser = 0.1
        self.chaserDelay = ((self.maxTimeDelayChaser-self.minTimeDelayChaser)/2+self.minTimeDelayChaser)//1
        self.maxTimeDelayRainbow = 1
        self.minTimeDelayRainbow = 0.1
        self.rainbowDelay = ((self.maxTimeDelayRainbow-self.minTimeDelayRainbow)/2+self.minTimeDelayRainbow)//1

        self.visualLightDisplay = visualLightDisplay
        self.lightDisplay = lightDisplay
        self.selectedLights = selectedLights
        self.effectIndividually = True
        self.runningChaser = False
        self.lightDisplay.chaseOn = False
        if len(self.selectedLights) == 0 and self.initialTime == False:
            self.errorWindow = ErrorWindow("You have not selected any lights to do effects with")
            self.close()
        self.setGeometry(int(xpos),int(ypos),int(width),int(height)) #sets window parameters top left is (0,0)
        self.setWindowTitle("Effects") #sets window title
        self.initUI()
    def initUI(self):
        self.effectAsGroupButton = QPushButton(self)
        self.effectAsGroupButton.setCheckable(True)
        self.effectAsGroupButton.move(50,50)
        self.effectAsGroupButton.setFixedWidth(200)
        self.effectAsGroupButton.setText("Set effect as Group")
        self.effectAsGroupButton.setStyleSheet("background-color:lightgrey")
        self.effectAsGroupButton.clicked.connect(self.effectAsGroupButtonClicked)

        self.effectIndividuallyButton = QPushButton(self)
        self.effectIndividuallyButton.setCheckable(True)
        self.effectIndividuallyButton.move(250,50)
        self.effectIndividuallyButton.setFixedWidth(200)
        self.effectIndividuallyButton.setText("Set effect as Group")
        self.effectIndividuallyButton.setStyleSheet("background-color:lightgrey")
        self.effectIndividuallyButton.clicked.connect(self.effectIndividuallyButtonClicked)
        # self.effectIndividuallyButtonClicked()

        self.chaserIO = self.createWholeSlider("Chaser",300,300,100,0,50) #the min max and start are percentages so 0 50 and 100%
        self.chaserIO[0].clicked.connect(self.toggleChaser)
        self.chaserIO[1].valueChanged[int].connect(self.chaserSliderChangedValue)
        self.chaserIO[2].textEdited.connect(self.chaserTextBoxChangedValue)

        self.rainbowIO = self.createWholeSlider("Rainbow",450,300,100,0,50) #the min max and start are percentages so 0 50 and 100%
        self.rainbowIO[0].clicked.connect(self.toggleRainbow)
        self.rainbowIO[1].valueChanged[int].connect(self.rainbowSliderChangedValue)
        self.rainbowIO[2].textEdited.connect(self.rainbowTextBoxChangedValue)

    def checkNumberOfLights(self):
        if len(self.selectedLights) == 0:
            self.errorWindow = ErrorWindow("You have not selected any lights to do effects with")
            self.close()

    def chaserTextBoxChangedValue(self):
        textBox = self.sender()
        try:
            textValue = textBox.text()[:]  ##[:] ensures that its a copy so it dosent cahnge the value inside the textBox
            textValue = int(textValue)
            if textValue>100:
                textBox.setText("100")
            elif textValue<0:
                textBox.setText("0")
            self.chaserIO[1].setValue(textValue)
        except:
            textBox.setText("")

    def rainbowTextBoxChangedValue(self):
        textBox = self.sender()
        try:
            textValue = textBox.text()[:]  ##[:] ensures that its a copy so it dosent cahnge the value inside the textBox
            textValue = int(textValue)
            if textValue>100:
                textBox.setText("100")
            elif textValue<0:
                textBox.setText("0")
            self.rainbowIO[1].setValue(textValue)
        except:
            textBox.setText("")



    def chaserSliderChangedValue(self):
        speedPercentage = (100-(self.chaserIO[1].value()))/100
        self.chaserIO[2].setText(str(int(round((1-speedPercentage)*100,0))))
        self.chaserDelay = (speedPercentage * (self.maxTimeDelayChaser-self.minTimeDelayChaser) + self.minTimeDelayChaser)//1

    def rainbowSliderChangedValue(self):
        speedPercentage = (100-(self.rainbowIO[1].value()))/100
        self.rainbowIO[2].setText(str(int(round((1-speedPercentage)*100,0))))
        self.rainbowDelay = (speedPercentage * (self.maxTimeDelayRainbow-self.minTimeDelayRainbow) + self.minTimeDelayRainbow)//1


    def createWholeSlider(self,effectName,xPos,yPos,maxVal,minVal,sliderStartValue):
        self.newButton = self.generateEffectButton(effectName,xPos-35,yPos+250)
        self.newSlider = self.generateSlider(maxVal,minVal,sliderStartValue,xPos,yPos)
        self.newTextBox = self.generateTextBox(xPos,yPos,"Speed")
        return [self.newButton,self.newSlider,self.newTextBox]

    def generateTextBox(self,startX,startY,textMessage):
        self.newTextBox = QLineEdit(self)
        self.newTextBox.move((startX-35),(startY+215))
        self.newTextBox.setPlaceholderText(textMessage) #sets the message of the text box before any text is entered
        self.newTextBox.setAlignment(Qt.AlignCenter)
        self.newTextBox.setFixedWidth(100)
        return self.newTextBox

    def generateSlider(self,maxVal,minVal,sliderStartValue,startX,startY):
        self.newSlider = QSlider(Qt.Vertical,self)
        self.newSlider.setMaximum(maxVal)
        self.newSlider.setMinimum(minVal)
        self.newSlider.setValue(int(sliderStartValue))
        self.newSlider.setGeometry(30,40,30,200)
        self.newSlider.move(startX,startY)
        return self.newSlider


    def generateEffectButton(self,effectName,xPos,yPos):
        self.newButton = QPushButton(self)
        self.newButton.move(xPos,yPos)
        self.newButton.setFixedSize(100,50)
        self.newButton.setText(effectName)
        self.newButton.setCheckable(True)
        self.newButton.setStyleSheet("background-color:white")
        return self.newButton

    def toggleChaser(self):
        if self.lightDisplay.runningChaser == False:
            self.lightDisplay.runningChaser = True
            self.lightDisplay.selectedLights = self.selectedLights
        else:
            self.lightDisplay.runningChaser = False
            for displayLight in self.lightDisplay.selectedLights:
                for light in self.lightDisplay.lights:
                    if light.startChannel == displayLight.channelNumber:
                        light.setToOrigional()
                        displayLight.changeColourAccordingToFixture()

    def toggleRainbow(self):
        if self.lightDisplay.runningRainbow == False:
            self.lightDisplay.runningRainbow = True
            self.lightDisplay.selectedLights = self.selectedLights
        else:
            self.lightDisplay.runningRainbow = False

    def effectAsGroupButtonClicked(self):
        button = self.sender()
        if button.isChecked():
            self.effectIndividually = False
            button.setStyleSheet("background-color:lightblue")
            self.effectIndividuallyButton.setStyleSheet("background-color;lightgrey")
            self.effectIndividuallyButton.setChecked(False)
        else:
            self.effectIndividually = True
            button.setStyleSheet("background-color:lightgrey")
            self.effectIndividuallyButton.setStyleSheet("background-color;lightblue")
            self.effectIndividuallyButton.setChecked(True)

    def effectIndividuallyButtonClicked(self):
        button = self.sender()
        if button.isChecked():
            self.effectIndividually = True
            button.setStyleSheet("background-color:lightblue")
            self.effectAsGroupButton.setStyleSheet("background-color;lightgrey")
            self.effectAsGroupButton.setChecked(False)
        else:
            self.effectIndividually = False
            button.setStyleSheet("background-color:lightgrey")
            self.effectAsGroupButton.setStyleSheet("background-color;lightblue")
            self.effectAsGroupButton.setChecked(True)
