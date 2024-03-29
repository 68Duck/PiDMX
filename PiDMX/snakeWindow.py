from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import random
import os

from errorWindow import ErrorWindow

class SnakeWindow(QWidget,uic.loadUiType(os.path.join("ui","snakeWindow.ui"))[0]):
    def __init__(self,lightDisplay,visualLightDisplay):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Snake Game")
        width = self.size().width()
        height = self.size().height()
        self.setGeometry(0,0,width,height)
        self.lightDisplay = lightDisplay
        self.visualLightDisplay = visualLightDisplay
        self.timer = QTimer()
        self.timer.timeout.connect(self.moveSnake)
        self.initUI()

    def getLEDBarInformation(self):
        channelNumbers = []
        for light in self.visualLightDisplay.lightList:
            if light.lightType == "LEDBar24ChannelMode":
                channelNumbers.append(light.channelNumber)
        if len(channelNumbers)>=1:
            channelNumbers.sort()
            firstChannel = channelNumbers[0]
            if len(channelNumbers)>1:
                secondChannel = channelNumbers[1]
                channelGap = secondChannel-firstChannel-24
            else:
                channelGap = 0
            numberOfBars = len(channelNumbers)
            return [firstChannel,channelGap,numberOfBars]
        else:
            return [None,None,None]


    def initUI(self):
        firstChannel,channelGap,numberOfBars = self.getLEDBarInformation()
        print(firstChannel,channelGap,numberOfBars)
        if firstChannel is None:
            self.startChannelInput.setText(str(100))
            self.channelGapInput.setText(str(0))
            self.numberLEDBarsInput.setText(str(8))
        else:
            self.startChannelInput.setText(str(firstChannel))
            self.channelGapInput.setText(str(channelGap))
            self.numberLEDBarsInput.setText(str(numberOfBars))
        self.startGameButton.clicked.connect(self.startButtonPressed)
        self.firstChannel = int(self.startChannelInput.text())  #this is the first channel of the first LED Bar
        self.channelGap = int(self.channelGapInput.text())
        self.noBars = int(self.numberLEDBarsInput.text())

    def startButtonPressed(self):
        self.firstChannel = int(self.startChannelInput.text())  #this is the first channel of the first LED Bar
        self.channelGap = int(self.channelGapInput.text())
        self.noBars = int(self.numberLEDBarsInput.text())
        self.snake = Snake(self)

        self.snakeSpeed = 500
        self.timer.start(self.snakeSpeed)
        self.pelletX = random.randint(0,self.noBars)
        self.pelletY = random.randint(0,7)
        self.finished = False

    def moveSnake(self):
        # print(self.snake.bodyPieces[0].xPos,self.snake.bodyPieces[0].yPos)
        self.snake.move()
        self.updateSnakeBoard()

    def updateSnakeBoard(self):
        if not self.finished:
            self.lightDisplay.universeLock = True
            for i in range(24*self.noBars):
                self.lightDisplay.updateChannel(i+self.firstChannel+(i*self.channelGap)//24,0)
                # self.lightDisplay.universeChannelValues[i+self.firstChannel+(i*self.channelGap)//24] = 0
            # counter = 0
            self.initialiseRainbow()
            for bodyPiece in self.snake.bodyPieces:
                self.runRainbow()
                redChannelNumber = self.firstChannel + (bodyPiece.xPos)*(24) + bodyPiece.xPos*self.channelGap + bodyPiece.yPos*3
                greenChannelNumber = redChannelNumber + 1
                blueChannelNumber = greenChannelNumber + 1
                self.lightDisplay.updateChannel(redChannelNumber,self.redRainbow) 
                self.lightDisplay.updateChannel(greenChannelNumber,self.greenRainbow)
                self.lightDisplay.updateChannel(blueChannelNumber,self.blueRainbow)
                # self.lightDisplay.universeChannelValues[redChannelNumber] = self.redRainbow
                # self.lightDisplay.universeChannelValues[greenChannelNumber] = self.greenRainbow
                # self.lightDisplay.universeChannelValues[blueChannelNumber] = self.blueRainbow
                # counter += 1

            redChannelNumber = self.firstChannel + self.pelletX*(24) + self.pelletX*self.channelGap + self.pelletY*3  #turn on pellet light
            greenChannelNumber = redChannelNumber + 1
            blueChannelNumber = greenChannelNumber + 1
            self.lightDisplay.updateChannel(redChannelNumber,3)
            self.lightDisplay.updateChannel(greenChannelNumber,255)
            self.lightDisplay.updateChannel(blueChannelNumber,3)
            # self.lightDisplay.universeChannelValues[redChannelNumber] = 3
            # self.lightDisplay.universeChannelValues[greenChannelNumber] = 255
            # self.lightDisplay.universeChannelValues[blueChannelNumber] = 3

            for light in self.lightDisplay.lights:
                light.updateChannelValuesFromUniverse()
                light.updateChannelValues()
            self.lightDisplay.universeLock = False
            self.lightDisplay.universeChanged()
            for light in self.visualLightDisplay.lightList:
                light.changeColourAccordingToFixture()
            self.lightDisplay.universeLock = False


    def runRainbow(self):
        if True:
            if self.redIncreasing:
                if self.redRainbow+self.rainbowChangeAmount > 255:
                    self.redIncreasing = False
                    self.blueDecreasing = True
                else:
                    self.redRainbow += self.rainbowChangeAmount
            if self.redDecreasing:
                if self.redRainbow-self.rainbowChangeAmount < 0:
                    self.redDecreasing = False
                    self.blueIncreasing = True
                else:
                    self.redRainbow -= self.rainbowChangeAmount
            if self.greenIncreasing:
                if self.greenRainbow+self.rainbowChangeAmount > 255:
                    self.greenIncreasing = False
                    self.redDecreasing = True
                else:
                    self.greenRainbow += self.rainbowChangeAmount
            if self.greenDecreasing:
                if self.greenRainbow-self.rainbowChangeAmount <= 0:
                    self.greenDecreasing = False
                    self.redIncreasing = True
                else:
                    self.greenRainbow -= self.rainbowChangeAmount
            if self.blueIncreasing:
                if self.blueRainbow+self.rainbowChangeAmount >= 255:
                    self.blueIncreasing = False
                    self.greenDecreasing = True
                else:
                    self.blueRainbow += self.rainbowChangeAmount
            if self.blueDecreasing:
                if self.blueRainbow-self.rainbowChangeAmount <= 0:
                    self.blueDecreasing = False
                    self.greenIncreasing = True
                else:
                    self.blueRainbow -= self.rainbowChangeAmount


    def initialiseRainbow(self):
        self.redIncreasing = False
        self.greenIncreasing = True
        self.blueIncreasing = False
        self.redDecreasing = False
        self.greenDecreasing = False
        self.blueDecreasing = False
        self.redRainbow = 255
        self.greenRainbow = 0
        self.blueRainbow = 0
        self.rainbowChangeAmount = 25


    def keyPressEvent(self,e):
        if e.key() == Qt.Key_W:
            self.snake.heading="u"
        elif e.key() == Qt.Key_A:
            self.snake.heading="l"
        elif e.key() == Qt.Key_S:
            self.snake.heading="d"
        elif e.key() == Qt.Key_D:
            self.snake.heading="r"

    def closeEvent(self,*args,**kargs):
        self.lightDisplay.universeLock = True
        for i in range(24*self.noBars):
            self.lightDisplay.universeChannelValues[i+self.firstChannel+(i*self.channelGap)//24] = 255
        for light in self.lightDisplay.lights:
            light.updateChannelValuesFromUniverse()
            light.updateChannelValues()
        self.lightDisplay.universeLock = False
        self.lightDisplay.universeChanged()
        for light in self.visualLightDisplay.lightList:
            light.changeColourAccordingToFixture()
        self.lightDisplay.universeLock = False
        self.timer.stop()

class Snake(object):
    def __init__(self,window):
        self.window = window
        self.heading = "r"
        self.bodyPieces = [SnakeBody(0,0)]  #0 is the front of the snake
    def move(self):
        for i in range(len(self.bodyPieces)-1):  #0 is the front of the snake
            j = len(self.bodyPieces)-1-i
            self.bodyPieces[j].xPos = self.bodyPieces[j-1].xPos
            self.bodyPieces[j].yPos = self.bodyPieces[j-1].yPos
        if self.heading == "r":
            self.bodyPieces[0].xPos += 1
            if self.bodyPieces[0].xPos > self.window.noBars-1:  #as zero indexed
                self.bodyPieces[0].xPos = 0
        elif self.heading == "l":
            self.bodyPieces[0].xPos -= 1
            if self.bodyPieces[0].xPos < 0:
                self.bodyPieces[0].xPos = self.window.noBars-1  #0 indexed
        elif self.heading == "u":
            self.bodyPieces[0].yPos -= 1
            if self.bodyPieces[0].yPos < 0:  #as zero indexed
                self.bodyPieces[0].yPos = 7
        elif self.heading == "d":
            self.bodyPieces[0].yPos += 1
            if self.bodyPieces[0].yPos > 7:
                self.bodyPieces[0].yPos = 0  #0 indexed
        else:
            self.errorWindow = ErrorWindow("Heading not correctly defined.")

        for i in range(1,len(self.bodyPieces)):
            if self.bodyPieces[i].xPos == self.bodyPieces[0].xPos:
                if self.bodyPieces[i].yPos == self.bodyPieces[0].yPos:
                    self.window.finished = True
                    self.window.close()
                    self.errorWindow = ErrorWindow("You died")
                    return
        self.checkPellet()

    def checkPellet(self):
        for bodyPiece in self.bodyPieces:
            if bodyPiece.xPos == self.window.pelletX:
                if bodyPiece.yPos == self.window.pelletY:
                    pelletLocationValid = False
                    self.increaseSize()
                    while pelletLocationValid == False:
                        pelletLocationValid = True
                        self.window.pelletX = random.randint(0,self.window.noBars-1)
                        self.window.pelletY = random.randint(0,7)
                        for bodyPiece in self.bodyPieces:
                            if bodyPiece.xPos == self.window.pelletX:
                                if bodyPiece.yPos == self.window.pelletY:
                                    pelletLocationValid = False

    def increaseSize(self):
        self.newBody = SnakeBody(self.bodyPieces[len(self.bodyPieces)-1].xPos,self.bodyPieces[len(self.bodyPieces)-1].yPos)
        # self.move()
        self.bodyPieces.append(self.newBody)



class SnakeBody(object):
    def __init__(self,xPos,yPos):  #xpos and ypos are 0 indexed
        self.xPos = xPos
        self.yPos = yPos
