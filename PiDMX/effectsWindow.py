from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from errorWindow import ErrorWindow

class EffectsWindow(QWidget,uic.loadUiType("effectsWindow.ui")[0]):
    def __init__(self,lightDisplay,selectedLights,visualLightDisplay,initialTime = False):
        super().__init__()
        self.setupUi(self)
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
        self.setWindowTitle("Effects") #sets window title
        self.initUI()
    def initUI(self):

        self.chaserButton.clicked.connect(self.toggleChaser)
        self.chaserButton.setCheckable(True)
        self.chaserSlider.valueChanged[int].connect(self.chaserSliderChangedValue)
        self.chaserText.textEdited.connect(self.chaserTextBoxChangedValue)
        self.chaserText.setPlaceholderText("Chaser")

        self.rainbowButton.clicked.connect(self.toggleRainbow)
        self.rainbowButton.setCheckable(True)
        self.rainbowSlider.valueChanged[int].connect(self.rainbowSliderChangedValue)
        self.rainbowText.textEdited.connect(self.rainbowTextBoxChangedValue)
        self.rainbowText.setPlaceholderText("Chaser")

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
            self.chaserSlider.setValue(textValue)
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
            self.rainbowSlider.setValue(textValue)
        except:
            textBox.setText("")



    def chaserSliderChangedValue(self):
        speedPercentage = (100-(self.chaserSlider.value()))/100
        self.chaserText.setText(str(int(round((1-speedPercentage)*100,0))))
        self.chaserDelay = (speedPercentage * (self.maxTimeDelayChaser-self.minTimeDelayChaser) + self.minTimeDelayChaser)//1

    def rainbowSliderChangedValue(self):
        speedPercentage = (100-(self.rainbowSlider.value()))/100
        self.rainbowText.setText(str(int(round((1-speedPercentage)*100,0))))
        self.rainbowDelay = (speedPercentage * (self.maxTimeDelayRainbow-self.minTimeDelayRainbow) + self.minTimeDelayRainbow)//1


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
