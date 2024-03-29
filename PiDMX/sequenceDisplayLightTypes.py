from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import math as maths

from os import path
from update_stylesheet import update_stylesheet

class SequenceParentDisplayLight(QWidget):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        super().__init__()
        self.lightType = addingLightType
        self.lightName = lightName
        self.lightDisplay = lightDisplay
        self.sequenceWindow = sequenceWindow
        self.xPos = xPos
        self.yPos = yPos
        self.red,self.green,self.blue = [255,255,255]
        self.shapes = self.createShapes()
        self.move()
        self.setClickableRegion()

    def remove(self):
        for shape in self.shapes:
            shape.hide()

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

    def convertColour(self,colour):
        red = colour.red()
        green = colour.green()
        blue = colour.blue()
        self.red = red
        self.green = green
        self.blue = blue
        red = hex(red)
        red = red[2:len(red)]
        if len(red) < 2:
            red = "0"+red
        green = hex(green)
        green = green[2:len(green)]
        if len(green) < 2:
            green = "0"+green
        blue = hex(blue)
        blue = blue[2:len(blue)]
        if len(blue) < 2:
            blue = "0"+blue
        colour = str(red)+str(green)+str(blue)
        return colour

    def convertColourRGB(self,rgb):
        rgb = int(rgb)
        rgb = hex(rgb)
        rgb = rgb[2:len(rgb)]
        if len(rgb) < 2:
            rgb = "0"+rgb
        return str(rgb)

    def changeColourRGB(self,red=None,green=None,blue=None):
        pass

    def setClickableRegion(self):
        pass

    def createShapes(self):
        pass

    def move(self):
        pass

    def changeColour(self,colour):  #colour in the form RGB
        self.red = colour[0]
        self.greeen = colour[1]
        self.blue = colour[2]

class DatabaseSequenceDisplayLight(SequenceParentDisplayLight):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        self.channelNumber = lightName[len(addingLightType):len(lightName)]
        self.indicators = []
        for light in lightDisplay.lights:
            if int(self.channelNumber) == int(light.startChannel):
                self.light = light
                self.lightInformation = light.lightInformation
                try:
                    a = self.lightInformation
                except:
                    raise Exception("There is no lightInformation")
        SequenceParentDisplayLight.__init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType)


    def createShapes(self):
        self.imageLabel = QLabel(self.sequenceWindow)
        pixmap = QPixmap(path.join("images",self.lightInformation["imageName"]))
        self.imageLabel.setPixmap(pixmap.scaled(100,100,Qt.KeepAspectRatio))
        self.imageLabel.setFixedSize(100,100)
        shapes = [self.imageLabel]

        for indicator in self.lightInformation["indicators"]:
            self.indicatorLabel = QLabel(self.sequenceWindow)
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

    def setClickableRegion(self):
        self.clickableLeft = 0
        self.clickableRight = 100
        self.clickableTop = 0
        self.clickableBottom = 100



    def move(self):
        self.imageLabel.move(self.xPos,self.yPos)
        for shape in self.shapes:
            if shape != self.imageLabel:
                shape.move(self.xPos+shape.relativeX,self.yPos+shape.relativeY)

        for shape in self.shapes:
            shape.show()

    def changeColourRGB(self,red=None,green=None,blue=None):
        if red == None:
            red = self.red
        else:
            self.red = red
        if green == None:
            green = self.green
        else:
            self.green = green
        if blue == None:
            blue = self.blue
        else:
            self.blue = blue
        red = self.convertColourRGB(red)
        green = self.convertColourRGB(green)
        blue = self.convertColourRGB(blue)
        colour = str(red)+str(green)+str(blue)
        for indicator in self.indicators:
            indicator.setStyleSheet(update_stylesheet(indicator.styleSheet(),"background-color",f'#{colour}'))
            indicator.setStyleSheet(update_stylesheet(indicator.styleSheet(),"border",f'3px solid#{colour}'))

    def changeColour(self,colour):
        colour = self.convertColour(colour)
        for indicator in self.indicators:
            indicator.setStyleSheet(update_stylesheet(indicator.styleSheet(),"background-color",f'#{colour}'))
            indicator.setStyleSheet(update_stylesheet(indicator.styleSheet(),"border",f'3px solid#{colour}'))

    def changeColourAccordingToFixture(self):
        channelInformation = self.lightInformation["channelInformation"]
        isRGB = False
        if self.lightInformation["isRGB"] == "1":
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

class SequenceDisplayLight(SequenceParentDisplayLight):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        SequenceParentDisplayLight.__init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType)
        self.channelNumber = lightName[len(addingLightType):len(lightName)]
        # self.indicators = []
        for light in lightDisplay.lights:
            if int(self.channelNumber) == int(light.startChannel):
                self.light = light

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


    def createShape(self,xPos,yPos,width,height,borderWidth,circle = False):
        self.shape = QLabel(self.sequenceWindow)
        if circle:
            self.shape.borderWidth = borderWidth
            self.shape.setStyleSheet(f'background-color: white; border-radius: {borderWidth}px;border: 3px solid white;')
        else:
            self.shape.setStyleSheet(f'background-color: black; border-radius: {borderWidth}px;border: 3px solid white;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape

    def move(self):
        self.circle1.move(self.xPos,self.yPos)
        for i in range(2,6,1): #adds top left top right bottom right and bottom left circles
            circle = getattr(self,f"circle{i}")
            circle.move(self.xPos+(20*((-1)**(maths.cos((i-1)*maths.pi/2)>0))),self.yPos+20*((-1)**(i)))
        self.border.move(self.xPos-35,self.yPos-35)

    def changeColourRGB(self,red=None,green=None,blue=None):
        if red == None:
            red = self.red
        else:
            self.red = red
        if green == None:
            green = self.green
        else:
            self.green = green
        if blue == None:
            blue = self.blue
        else:
            self.blue = blue
        red = self.convertColourRGB(red)
        green = self.convertColourRGB(green)
        blue = self.convertColourRGB(blue)
        colour = str(red)+str(green)+str(blue)
        for i in range(5):
            self.shapes[1+i].setStyleSheet(f'background-color: #{colour}; border-radius: {self.circle1.borderWidth}px;border: 3px solid #{colour};')

    def changeColourAccordingToFixture(self):
        channelNumber = int(self.lightName[len(self.lightType):len(self.lightName)])
        for light in self.lightDisplay.lights:
            if channelNumber == light.startChannel:
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



    def changeColour(self,colour):
        colour = self.convertColour(colour)
        for i in range(5):
            self.shapes[1+i].setStyleSheet(f'background-color: #{colour}; border-radius: {self.circle1.borderWidth}px;border: 3px solid #{colour};')

class SequenceDisplayLight2Small(SequenceParentDisplayLight):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType,parentClass,boxNumber):
        self.setClickableRegion()
        SequenceParentDisplayLight.__init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType)
        self.parentClass = parentClass
        self.boxNumber = boxNumber
    def createShapes(self):
        self.box = self.createShape(self.xPos,self.yPos,20,20)
        return [self.box]

    def setClickableRegion(self):
        self.clickableLeft = 0
        self.clickableRight = 20
        self.clickableTop = 0
        self.clickableBottom = 20

    def createShape(self,xPos,yPos,width,height):
        self.shape = QLabel(self.sequenceWindow)
        self.shape.setStyleSheet(f'background-color: white;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape

    def move(self):
        self.box.move(self.xPos,self.yPos)

    def changeWholeColour(self,colour):
        for i in range(8):
            box = getattr(self.parentClass,f"box{i+1}")
            box.changeColour(colour)

    def changeColour(self,colour):
        colour = self.convertColour(colour)
        self.box.setStyleSheet(f'background-color: #{colour}; border-radius: {1}px;border: 3px solid #{colour};')

    def changeColourAccordingToFixture(self):
        channelNumber = int(self.lightName[len(self.lightType):len(self.lightName)])-3*(self.boxNumber-1)
        for light in self.lightDisplay.lights:
            if channelNumber == light.startChannel:
                self.red = getattr(light,f"red{self.boxNumber}")
                self.green = getattr(light,f"green{self.boxNumber}")
                self.blue = getattr(light,f"blue{self.boxNumber}")
                colour = self.hexValueForRGB(self.red,self.green,self.blue)
                self.box.setStyleSheet(f'background-color: #{colour};')

    def changeColourRGB(self,red=None,green=None,blue=None):
        if red == None:
            red = self.red
        else:
            self.red = red
        if green == None:
            green = self.green
        else:
            self.green = green
        if blue == None:
            blue = self.blue
        else:
            self.blue = blue
        red = self.convertColourRGB(red)
        green = self.convertColourRGB(green)
        blue = self.convertColourRGB(blue)
        colour = str(red)+str(green)+str(blue)
        self.box.setStyleSheet(f'background-color: #{colour}; border-radius: {1}px;border: 3px solid #{colour};')


class SequenceDisplayLight2(object):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        self.xPos = xPos
        self.yPos = yPos
        lightType = addingLightType
        channel = int(lightName[len(addingLightType):len(lightName)])
        for i in range(8):
            setattr(self,f"box{i+1}",SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+3*i),self.xPos,self.yPos+20*i,addingLightType,self,i+1))


class SequenceDisplayLight3(SequenceParentDisplayLight):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        SequenceParentDisplayLight.__init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType)

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

    def createShape(self,xPos,yPos,width,height,border=False):
        self.shape = QLabel(self.sequenceWindow)
        if border:
            self.shape.setStyleSheet(f'background-color: white;')
        else:
            self.shape.setStyleSheet(f'background-color: black;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape

    def move(self):
        self.border.move(self.xPos,self.yPos)
        self.box.move(self.xPos+5,self.yPos+5)
        self.indicator.move(self.xPos+5,self.yPos)

    def changeColour(self,colour):
        intensity = colour.red  #just so it works with generic dimmers.
        self.red = intensity #just so it works with generic dimmers.
        self.indicator.setStyleSheet(f'background-color: rgba(255,255,0,{intensity});')

    def changeColourAccordingToFixture(self):
        channelNumber = int(self.lightName[len(self.lightType):len(self.lightName)])
        for fixture in self.lightDisplay.lights:
            if channelNumber == fixture.startChannel:
                intensity = fixture.intensity
                self.red = intensity
                self.indicator.setStyleSheet(f'background-color: rgba(255,255,0,{intensity});')

    def changeColourRGB(self,red=None,green=None,blue=None):
        self.indicator.setStyleSheet(f'background-color: rgba(255,255,0,{self.red});')

class SequenceDisplayLight4(SequenceParentDisplayLight): #miniscan
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        SequenceParentDisplayLight.__init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType)

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

    def createShape(self,xPos,yPos,width,height,border=False):
        self.shape = QLabel(self.sequenceWindow)
        if border:
            self.shape.setStyleSheet(f'background-color: white;')
        else:
            self.shape.setStyleSheet(f'background-color: black;')
        self.shape.move(xPos,yPos)
        self.shape.setFixedSize(width,height)
        self.shape.show()
        return self.shape
    def move(self):
        self.box.move(self.xPos,self.yPos)
        self.topOfIndicator.move(self.xPos+40,self.yPos)
        self.bottomOfIndicator.move(self.xPos+60,self.yPos+5)
        self.indicator.move(self.xPos+50,self.yPos+5)

    def changeColour(self,colour):
        pass

    def changeColourAccordingToFixture(self):
        channelNumber = int(self.lightName[len(self.lightType):len(self.lightName)])
        for fixture in self.lightDisplay.lights:
            if channelNumber == fixture.startChannel:
                intensity = fixture.intensity
                self.indicator.setStyleSheet(f'background-color: rgba(255,255,0,{intensity});')

    def changeColourRGB(self,red=None,green=None,blue=None):
        # self.indicator.setStyleSheet(f'background-color: rgba(255,255,0,{self.red});')
        pass
