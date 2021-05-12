from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from os import path
from update_stylesheet import update_stylesheet

class DisplayLightParent(object):
    def __init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow):
        self.selected = False
        self.setClickableRegion()
        self.lightDisplay = lightDisplay
        self.channelNumber = channelNumber
        self.light = False
        for light in self.lightDisplay.lights:
            if self.channelNumber == light.startChannel:
                self.light = light
        self.parentWindow = parentWindow
        self.xPos = xPos
        self.yPos = yPos
        self.shapes = self.createShapes()
        self.move()
        self.changeColourAccordingToFixture()

    def toggleSelected(self):
        pass #create the border if selected

    def move(self):
        pass #move each shape into the create place

    def changeColourAccordingToFixture(self):
        if self.light:
            self.changeColour()
        return True

    def changeColour(self):
        pass #change colour based on the colour based on the colour of the fixture

    def hide(self):
        for shape in self.shapes:
            shape.hide()

    def setClickableRegion():
        pass #set the clickable region

    def createShapes(self):
        return [] #create the shapes that create the light abstraction on screen. return the shapes in an array



class DisplayLight2(DisplayLightParent):
    def __init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow):
        DisplayLightParent.__init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow)

    def createShapes(self):
        for i in range(1,9,1):
            setattr(self,f"box{i}",self.createShape(self.xPos,self.yPos,20,20))
        return [self.box1,self.box2,self.box3,self.box4,self.box5,self.box6,self.box7,self.box8]

    def setClickableRegion(self):
        self.clickableLeft = 0
        self.clickableRight = 20
        self.clickableTop = 0
        self.clickableBottom = 175

    def hexValueForChannel(self,channel):
        channel = hex(channel)
        channel = channel[2:len(channel)]
        if len(channel) < 2:
            channel = "0" + channel
        return str(channel)

    def hexValueForRGB(self,red,green,blue):
        red = self.hexValueForChannel(red)
        green = self.hexValueForChannel(green)
        blue = self.hexValueForChannel(blue)
        return red+green+blue

    def changeColour(self):
        for i in range(1,9,1):
            box = getattr(self,f"box{i}")
            light = getattr(self,"light")
            colour = self.hexValueForRGB(getattr(light,f"red{i}"),getattr(light,f"green{i}"),getattr(light,f"blue{i}"))
            box.setStyleSheet(f'background-color: #{colour};')

    def move(self):
        for i in range(8):
            box = getattr(self,f"box{i+1}")
            box.move(self.xPos,self.yPos+20*i)

    def createShape(self,xPos,yPos,width,height):
        self.shape = QLabel(self.parentWindow)
        self.shape.setStyleSheet(f'background-color: white;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape

    def toggleSelected(self):
        if self.selected:
            self.selected = False
            self.changeColour()
            self.selectedShape.hide()
        else:
            self.selected = True
            self.selectedShape = QLabel(self.parentWindow)
            self.selectedShape.move(self.xPos-5,self.yPos-5)
            self.selectedShape.setStyleSheet("border: 1px solid orange; background-color:transparent")
            self.selectedShape.setFixedSize(30,170)
            self.selectedShape.show()


class DatabaseDisplayLight(DisplayLightParent): #finish me
    def __init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow):
        # QLabel.__init__(self)
        self.indicators = []
        for light in parentWindow.lightDisplay.lights:
            if channelNumber == light.startChannel:
                self.lightInformation = light.lightInformation
                try:
                    a = self.lightInformation
                except:
                    raise Exception("There is no lightInformation")
        DisplayLightParent.__init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow)

    def changeColour(self):
        channelInformation = self.lightInformation["channelInformation"]
        isRGB = False
        if self.lightInformation["isRGB"]:
            isRGB = True
        for channel in channelInformation:
            if channel["channelInformation"] is not None:
                if isRGB:
                    if channel["channelInformation"] == "red":
                        redChannelName = channel["channelName"]
                    if channel["channelInformation"] == "green":
                        greenChannelName = channel["channelName"]
                    if channel["channelInformation"] == "blue":
                        blueChannelName = channel["channelName"]
                else:
                    if channel["channelInformation"] == "intensity":
                        intensityChannelName = channel["channelName"]

        light = getattr(self,"light")
        if isRGB:
            colour = self.hexValueForRGB(getattr(light,redChannelName),getattr(light,greenChannelName),getattr(light,blueChannelName))
            for indicator in self.indicators:
                indicator.setStyleSheet(update_stylesheet(indicator.styleSheet(),"background-color",f'#{colour}'))
                indicator.setStyleSheet(update_stylesheet(indicator.styleSheet(),"border",f'3px solid#{colour}'))
        else:
            #finish me
            for indicator in self.indicators:
                styleSheet = indicator.styleSheet() + f'background-color: rgba(255,255,0,{getattr(light,intensityChannelName)});'
                indicator.setStyleSheet(styleSheet)
                # indicator.setStyleSheet(indicator.styleSheet().append(QString(f'background-color: rgba(255,255,0,{getattr(light,intensityChannelName)});')))



    def hexValueForChannel(self,channel):
        channel = hex(channel)
        channel = channel[2:len(channel)]
        if len(channel) < 2:
            channel = "0" + channel
        return str(channel)

    def hexValueForRGB(self,red,green,blue):
        red = self.hexValueForChannel(red)
        green = self.hexValueForChannel(green)
        blue = self.hexValueForChannel(blue)
        return red+green+blue

    def move(self):
        self.imageLabel.move(self.xPos,self.yPos)
        for shape in self.shapes:
            if shape != self.imageLabel:
                shape.move(self.xPos+shape.relativeX,self.yPos+shape.relativeY)

        for shape in self.shapes:
            shape.show()

    def setClickableRegion(self):
        self.clickableLeft = 0
        self.clickableRight = 100
        self.clickableTop = 50
        self.clickableBottom = 50

    def createShapes(self):
        self.imageLabel = QLabel(self.parentWindow)
        pixmap = QPixmap(path.join("images",self.lightInformation["imageName"]))
        self.imageLabel.setPixmap(pixmap.scaled(100,100,Qt.KeepAspectRatio))
        self.imageLabel.setFixedSize(100,100)
        shapes = [self.imageLabel]

        for indicator in self.lightInformation["indicators"]:
            self.indicatorLabel = QLabel(self.parentWindow)
            x = indicator["x"]//5
            y = indicator["y"]//5
            width = indicator["width"]//5
            height = indicator["height"]//5
            type = indicator["type"]
            self.indicatorLabel.relativeX = x
            self.indicatorLabel.relativeY = y
            self.indicatorLabel.setFixedSize(width,height)
            if type == "circle":
                self.indicatorLabel.setStyleSheet(f"background-color:#ffff00;border-radius:{int(width/2)};border: 3px solid #ffff00;")
            elif type == "square":
                self.indicatorLabel.setStyleSheet(f"background-color:#ffff00;border: 3px solid #ffff00;")
            shapes.append(self.indicatorLabel)
            self.indicators.append(self.indicatorLabel)

        return shapes

class DisplayLight(DisplayLightParent): #rgbLight
    def __init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow):
        DisplayLightParent.__init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow)

    def createShapes(self):
        self.border = self.createShape(self.xPos-35,self.yPos-35,80,80,20)
        for i in range(1,6,1):
            setattr(self,f"circle{i}",self.createShape(self.xPos,self.yPos,10,10,int(10/2),True))
        return [self.border,self.circle1,self.circle2,self.circle3,self.circle4,self.circle5]

    def setClickableRegion(self):
        self.clickableLeft = 40
        self.clickableRight = 40
        self.clickableTop = 40
        self.clickableBottom = 40

    def changeColour(self):
        red = hex(self.light.red)
        red = red[2:len(red)]
        if len(red) < 2:
            red = "0"+red
        green = hex(self.light.green)
        green = green[2:len(green)]
        if len(green) < 2:
            green = "0"+green
        blue = hex(self.light.blue)
        blue = blue[2:len(blue)]
        if len(blue) < 2:
            blue = "0"+blue
        colour = str(red)+str(green)+str(blue)
        for i in range(5):
            self.shapes[1+i].setStyleSheet(f'background-color: #{colour}; border-radius: {self.circle1.borderWidth}px;border: 3px solid #{colour};')  #all borderwidths should be the same

    def move(self):
        self.circle1.move(self.xPos,self.yPos)
        self.circle2.move(self.xPos-20,self.yPos-20)
        self.circle3.move(self.xPos-20,self.yPos+20)
        self.circle4.move(self.xPos+20,self.yPos-20)
        self.circle5.move(self.xPos+20,self.yPos+20)
        self.border.move(self.xPos-35,self.yPos-35)
    def createShape(self,xPos,yPos,width,height,borderWidth,circle = False):
        self.shape = QLabel(self.parentWindow)
        if circle:
            self.shape.borderWidth = borderWidth
            self.shape.setStyleSheet(f'background-color: white; border-radius: {borderWidth}px;border: 3px solid white;')
        else:
            self.shape.setStyleSheet(f'background-color: black; border-radius: {borderWidth}px;border: 3px solid white;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape
    def toggleSelected(self):
        if self.selected:
            self.selected = False
            finished = self.changeColourAccordingToFixture()
            self.selectedShape.hide()
        else:
            self.selected = True
            self.selectedShape = QLabel(self.parentWindow)
            self.selectedShape.move(self.xPos-40,self.yPos-40)
            self.selectedShape.setStyleSheet("border: 1px solid orange; background-color:transparent")
            self.selectedShape.setFixedSize(90,90)
            self.selectedShape.show()


class DisplayLight3(DisplayLightParent): #generic dimmer
    def __init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow):
        DisplayLightParent.__init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow)

    def createShapes(self):
        self.border = self.createShape(self.xPos,self.yPos,35,75,border=True)
        self.box = self.createShape(self.xPos,self.yPos,25,65)
        self.indicator = self.createShape(self.xPos,self.yPos,25,20)
        return [self.border,self.box,self.indicator]

    def setClickableRegion(self):
        self.clickableLeft = 0
        self.clickableRight = 35
        self.clickableTop = 0
        self.clickableBottom = 75

    def changeColour(self):  #needs to be colour as this is how it is done in the parent class
        intensity = self.light.intensity
        self.indicator.setStyleSheet(f'background-color: rgba(255,255,0,{intensity});')
    def move(self):
        self.border.move(self.xPos,self.yPos)
        self.box.move(self.xPos+5,self.yPos+5)
        self.indicator.move(self.xPos+5,self.yPos)
    def createShape(self,xPos,yPos,width,height,border=False):
        self.shape = QLabel(self.parentWindow)
        if border:
            self.shape.setStyleSheet(f'background-color: white;')
        else:
            self.shape.setStyleSheet(f'background-color: black;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape

    def toggleSelected(self):
        if self.selected:
            self.selected = False
            finished = self.changeColourAccordingToFixture()
            self.selectedShape.hide()
        else:
            self.selected = True
            self.selectedShape = QLabel(self.parentWindow)
            self.selectedShape.move(self.xPos-5,self.yPos-5)
            self.selectedShape.setStyleSheet("border: 1px solid orange; background-color:transparent")
            self.selectedShape.setFixedSize(45,85)
            self.selectedShape.show()


class DisplayLight4(DisplayLightParent): #miniscan
    def __init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow):
        DisplayLightParent.__init__(self,xPos,yPos,channelNumber,lightDisplay,parentWindow)

    def createShapes(self):
        self.box = self.createShape(self.xPos,self.yPos,40,30,border=True)
        self.topOfIndicator = self.createShape(self.xPos,self.yPos,25,5,border=True)
        self.bottomOfIndicator = self.createShape(self.xPos,self.yPos,5,15,border=True)
        self.indicator = self.createShape(self.xPos,self.yPos,10,10)
        return [self.box,self.topOfIndicator,self.bottomOfIndicator,self.indicator]

    def setClickableRegion(self):
        self.clickableLeft = 0
        self.clickableRight = 70
        self.clickableTop = 0
        self.clickableBottom = 30

    def changeColour(self):  #needs to be colour as this is how it is done in the parent class
        intensity = self.light.intensity
        self.indicator.setStyleSheet(f'background-color: rgba(255,255,0,{intensity});')
    def move(self):
        self.box.move(self.xPos,self.yPos)
        self.topOfIndicator.move(self.xPos+40,self.yPos)
        self.bottomOfIndicator.move(self.xPos+60,self.yPos+5)
        self.indicator.move(self.xPos+50,self.yPos+5)
    def createShape(self,xPos,yPos,width,height,border=False):
        self.shape = QLabel(self.parentWindow)
        if border:
            self.shape.setStyleSheet(f'background-color: white;')
        else:
            self.shape.setStyleSheet(f'background-color: black;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape

    def toggleSelected(self):
        if self.selected:
            self.selected = False
            finished = self.changeColourAccordingToFixture()
            self.selectedShape.hide()
        else:
            self.selected = True
            self.selectedShape = QLabel(self.parentWindow)
            self.selectedShape.move(self.xPos-5,self.yPos-5)
            self.selectedShape.setStyleSheet("border: 1px solid orange; background-color:transparent")
            self.selectedShape.setFixedSize(80,40)
            self.selectedShape.show()
