from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*


class Light(object):
    def __init__(self,startChannel,infoMode = False):
        self.duplicate = False  #this is a duplicate or has a duplicate of it made.
        self.infoMode = infoMode
        self.startChannel = startChannel
        self.lightType="LightName"
        self.dropdownName = "DropDownName"
        self.lightDisplay = False
        self.initChannels()
    def initChannels(self):
        self.channels = []
        self.channelValues = []
        self.previousValues = self.channels
    def changeUniverse(self,updateUniverse=True):
        if self.lightDisplay == False:
            self.errorWindow = ErrorWindow("ERROR LightDisplay has not been defined")
        else:
            self.lightDisplay.universeLock = True
            for i in range(len(self.channelValues)):
                self.lightDisplay.universeChannelValues[self.startChannel+i] = self.channelValues[i]
            self.lightDisplay.universeLock = False
            if updateUniverse:
                self.lightDisplay.universeChanged()
    def updateChannelValuesFromUniverse(self):
        for i in range(len(self.channelValues)):
            self.channelValues[i] = self.lightDisplay.universeChannelValues[self.startChannel+i]
    def returnChannelValues(self):
        return self.channelValues
    def updateChannelValues(self):
        #put each variable name equal to the correct part of self.channelValues
        pass
    def generateNewLight(self,channel):
        newLight = Light(channel)  #change light for each class type
        return newLight
    def setToBlack(self):
        self.previousValues = []
        for channel in self.channelValues:
            self.previousValues.append(channel)
        for i in range(len(self.channelValues)):
            self.channelValues[i] = 0
        self.updateChannelValues()
        self.changeUniverse()
    def setToOrigional(self):
        for i in range(len(self.channelValues)):
            self.channelValues[i] = self.previousValues[i]  #previous values and channel values should be the same
        self.updateChannelValues()
        self.changeUniverse()

class Miniscan(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "Miniscan"
        self.dropdownName = "Miniscan"
        self.colour = 0 #so open
        self.goboRoation = 191 # so no rotation
        self.gobo = 0 # so open
        self.intensity = 255
        self.pan = 255//2
        self.tilt = 255//2
        self.effects = 0 #so open
        self.channels = ["Colour","Gobo Rotation","Gobo","Intensity","Pan","Tilt","Effects"]
        self.channelValues = [self.colour,self.goboRoation,self.gobo,self.intensity,self.pan,self.tilt,self.effects]
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        self.colour = self.channelValues[0]
        self.goboRoation = self.channelValues[1]
        self.gobo = self.channelValues[2]
        self.intensity = self.channelValues[3]
        self.pan = self.channelValues[4]
        self.tilt = self.channelValues[5]
        self.effects = self.channelValues[6]
    def generateNewLight(self,channel):
        newLight = Miniscan(channel)  #where NewLight is the class name but newLight is the variable newLight
        return newLight


class RGB6Channel(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "RGB6Channel"
        self.dropdownName = "RGB 6 Channel Light"
        self.intensity = 255
        self.red = 255
        self.green = 255
        self.blue = 255
        self.strobe = 0
        self.colourFade = 0
        self.channels = ["Intensity","Red","Green","Blue","Strobe","ColourFade"]
        self.channelValues = [self.intensity,self.red,self.green,self.blue,self.strobe,self.colourFade]
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        self.intensity = self.channelValues[0]
        self.red = self.channelValues[1]
        self.green = self.channelValues[2]
        self.blue = self.channelValues[3]
        self.strobe = self.channelValues[4]
        self.colourFade = self.channelValues[5]
    def generateNewLight(self,channel):
        newLight = RGB6Channel(channel)  #where NewLight is the class name but newLight is the variable newLight
        return newLight


class RGB8Channel(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "RGB8Channel"
        self.dropdownName = "RGB 8 Channel Light"
        self.intensity = 255
        self.red = 255
        self.green = 255
        self.blue = 255
        self.white = 0
        self.colourFader = 0
        self.colourChooser = 0
        self.strobe = 0
        self.channels = ["Intensity","Red","Green","Blue","White","ColourFader","ColourChooser","Strobe"]
        self.channelValues = [self.intensity,self.red,self.green,self.blue,self.white,self.colourFader,self.colourChooser,self.strobe]
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        self.intensity = self.channelValues[0]
        self.red = self.channelValues[1]
        self.green = self.channelValues[2]
        self.blue = self.channelValues[3]
        self.white = self.channelValues[4]
        self.colourFader = self.channelValues[5]
        self.colourChooser = self.channelValues[6]
        self.strobe = self.channelValues[7]
    def generateNewLight(self,channel):
        newLight = RGB8Channel(channel)  #where NewLight is the class name but newLight is the variable newLight
        return newLight


class RGBLight(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType="RGBLight"
        self.dropdownName = "RGB Light with intensity"
        self.intensity = 255
        self.red = 255
        self.green = 255
        self.blue = 255
        self.channels = ["Intensity","Red","Green","Blue"]
        self.channelValues = [self.intensity,self.red,self.green,self.blue]
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        self.intensity = self.channelValues[0]
        self.red = self.channelValues[1]
        self.green = self.channelValues[2]
        self.blue = self.channelValues[3]
    def generateNewLight(self,channel):
        newLight = RGBLight(channel)
        return newLight

class RGBWLight(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType="RGBWLight"
        self.dropdownName = "RGBW Light"
        self.red = 255
        self.green = 255
        self.blue = 255
        self.white = 0
        self.channels = ["Red","Green","Blue","White"]
        self.channelValues = [self.red,self.green,self.blue,self.white]
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        self.red = self.channelValues[0]
        self.green = self.channelValues[1]
        self.blue = self.channelValues[2]
        self.white = self.channelValues[3]
    def generateNewLight(self,channel):
        newLight = RGBWLight(channel)
        return newLight

class GenericDimmer(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "GenericDimmer"
        self.dropdownName = "Generic Dimmer"
        self.intensity = 255
        self.channels=["Intensity"]
        self.channelValues = [self.intensity]
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        self.intensity = self.channelValues[0]
    def generateNewLight(self,channel):
        newLight = GenericDimmer(channel)
        return newLight

class LEDBar24ChannelMode(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "LEDBar24ChannelMode"
        self.dropdownName = "LED bar 24 channel mode"
        colours = ["red","green","blue"]
        for i in range(1,9,1):
            for colour in colours:
                setattr(self,f"{colour}{i}",255)
                self.channelValues.append(getattr(self,f"{colour}{i}"))

        coloursCaptialised = ["Red","Green","Blue"]
        self.channels = []
        for i in range(1,9,1):
            for colour in coloursCaptialised:
                self.channels.append(f"{colour}{i}")
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        counter = 0
        colours = ["red","green","blue"]
        for i in range(1,9,1):
            for colour in colours:
                setattr(self,f"{colour}{i}",self.channelValues[counter])
                counter += 1
    def generateNewLight(self,channel):
        newLight = LEDBar24ChannelMode(channel)
        return newLight
