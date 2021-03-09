from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import random

from errorWindow import ErrorWindow

class SnakeWindow(QWidget):
    def __init__(self,lightDisplay,visualLightDisplay):
        super().__init__()
        self.setWindowTitle("Snake Game")
        self.setGeometry(0,0,100,100)
        self.firstChannel = 100  #this is the first channel of the first LED Bar
        self.lightDisplay = lightDisplay
        self.visualLightDisplay = visualLightDisplay
        self.snake = Snake(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.moveSnake)
        self.snakeSpeed = 500
        self.timer.start(self.snakeSpeed)
        self.pelletX = random.randint(0,7)
        self.pelletY = random.randint(0,7)
        self.finished = False
        self.initUI()

    def initUI(self):
        self.l = QLabel(self)
        self.l.setText("Use the w,a,s,d")
        self.l2 = QLabel(self)
        self.l2.setText("keys to move the")
        self.l3 = QLabel(self)
        self.l3.setText("snake around the board")
        self.l.move(5,0)
        self.l2.move(5,20)
        self.l3.move(5,40)

    def moveSnake(self):
        # print(self.snake.bodyPieces[0].xPos,self.snake.bodyPieces[0].yPos)
        self.snake.move()
        self.updateSnakeBoard()

    def updateSnakeBoard(self):
        if not self.finished:
            self.lightDisplay.universeLock = True
            for i in range(24*8):
                self.lightDisplay.universeChannelValues[i+self.firstChannel] = 10
            for bodyPiece in self.snake.bodyPieces:
                redChannelNumber = self.firstChannel + bodyPiece.xPos*24 + bodyPiece.yPos*3
                greenChannelNumber = redChannelNumber + 1
                blueChannelNumber = greenChannelNumber + 1
                self.lightDisplay.universeChannelValues[redChannelNumber] = 255
                self.lightDisplay.universeChannelValues[greenChannelNumber] = 3
                self.lightDisplay.universeChannelValues[blueChannelNumber] = 7

            redChannelNumber = self.firstChannel + self.pelletX*24 + self.pelletY*3  #turn on pellet light
            greenChannelNumber = redChannelNumber + 1
            blueChannelNumber = greenChannelNumber + 1
            self.lightDisplay.universeChannelValues[redChannelNumber] = 3
            self.lightDisplay.universeChannelValues[greenChannelNumber] = 255
            self.lightDisplay.universeChannelValues[blueChannelNumber] = 3

            for light in self.lightDisplay.lights:
                light.updateChannelValuesFromUniverse()
                light.updateChannelValues()
            self.lightDisplay.universeLock = False
            self.lightDisplay.universeChanged()
            for light in self.visualLightDisplay.lightList:
                light.changeColourAccordingToFixture()
            self.lightDisplay.universeLock = False


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
        for i in range(24*8):
            self.lightDisplay.universeChannelValues[i+self.firstChannel] = 255
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
            if self.bodyPieces[0].xPos > 7:  #as zero indexed
                self.bodyPieces[0].xPos = 0
        elif self.heading == "l":
            self.bodyPieces[0].xPos -= 1
            if self.bodyPieces[0].xPos < 0:
                self.bodyPieces[0].xPos = 7  #0 indexed
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
                        self.window.pelletX = random.randint(0,7)
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
