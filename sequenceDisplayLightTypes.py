from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class SequenceParentDisplayLight(QWidget):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        super().__init__()
        self.lightType = addingLightType
        self.lightName = lightName
        self.lightDisplay = lightDisplay
        self.sequenceWindow = sequenceWindow
        self.xPos = xPos
        self.yPos = yPos
        self.red = 255
        self.green = 255
        self.blue = 255
        self.shapes = self.createShapes()
        self.move()
        self.setClickableRegion()

    def remove(self):
        for shape in self.shapes:
            shape.hide()

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

class SequenceDisplayLight(SequenceParentDisplayLight):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        SequenceParentDisplayLight.__init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType)

    def createShapes(self):
        self.border = self.createShape(self.xPos-35,self.yPos-35,80,80,20)
        self.circle1 = self.createShape(self.xPos,self.yPos,10,10,int(10/2),True)
        self.circle2 = self.createShape(self.xPos,self.yPos,10,10,int(10/2),True)
        self.circle3 = self.createShape(self.xPos,self.yPos,10,10,int(10/2),True)
        self.circle4 = self.createShape(self.xPos,self.yPos,10,10,int(10/2),True)
        self.circle5 = self.createShape(self.xPos,self.yPos,10,10,int(10/2),True)
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
        self.circle2.move(self.xPos-20,self.yPos-20)
        self.circle3.move(self.xPos-20,self.yPos+20)
        self.circle4.move(self.xPos+20,self.yPos-20)
        self.circle5.move(self.xPos+20,self.yPos+20)
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


    def changeColour(self,colour):
        colour = self.convertColour(colour)
        for i in range(5):
            self.shapes[1+i].setStyleSheet(f'background-color: #{colour}; border-radius: {self.circle1.borderWidth}px;border: 3px solid #{colour};')

class SequenceDisplayLight2Small(SequenceParentDisplayLight):
    def __init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType):
        self.setClickableRegion()
        SequenceParentDisplayLight.__init__(self,lightDisplay,sequenceWindow,lightName,xPos,yPos,addingLightType)

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

    def changeColour(self,colour):
        colour = self.convertColour(colour)
        self.box.setStyleSheet(f'background-color: #{colour}; border-radius: {1}px;border: 3px solid #{colour};')

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
        self.box1 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+0),self.xPos,self.yPos,addingLightType)
        self.box2 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+3),self.xPos,self.yPos+20,addingLightType)
        self.box3 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+6),self.xPos,self.yPos+40,addingLightType)
        self.box4 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+9),self.xPos,self.yPos+60,addingLightType)
        self.box5 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+12),self.xPos,self.yPos+80,addingLightType)
        self.box6 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+15),self.xPos,self.yPos+100,addingLightType)
        self.box7 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+18),self.xPos,self.yPos+120,addingLightType)
        self.box8 = SequenceDisplayLight2Small(lightDisplay,sequenceWindow,lightType+str(channel+21),self.xPos,self.yPos+140,addingLightType)


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
