from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from order_dictionaries import order_dictionaries

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
    def createChannelValues(self):
        self.channelValues = []
        for channel in self.channelNames:
            self.channelValues.append(getattr(self,channel))
        self.previousValues = self.channelValues
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
        for i in range(len(self.channelNames)):
            setattr(self,self.channelNames[i],self.channelValues[i])
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

class LightFromDatabase(Light): #Finish me
    def __init__(self,startChannel,infoMode = False,lightInformation = None):
        Light.__init__(self,startChannel,infoMode)
        if lightInformation is None:
            self.errorWindow = ErrorWindow("There is no information passed in to this light.")
        self.lightInformation = lightInformation
        # print(self.lightInformation)
        self.lightType = lightInformation["lightName"]
        self.dropdownName = self.lightType
        self.imageName = lightInformation["imageName"]
        self.isRGB = lightInformation["isRGB"]
        self.hasPanTilt = lightInformation["hasPanTilt"]
        self.indicators = lightInformation["indicators"]
        self.channelInformation = lightInformation["channelInformation"]
        self.channelNames = []
        self.channelInformation = order_dictionaries(self.channelInformation,"channelNumber")
        for channel in self.channelInformation:
            self.channelNames.append(channel["channelName"])
            setattr(self,channel["channelName"],channel["channelStartValue"])
            if channel["channelInformation"] != None:
                setattr(self,f"{channel['channelInformation']}channelName",channel["channelName"])

        print(self.channelNames)
        self.channels = self.channelNames
        self.createChannelValues()
    def generateNewight(self,channel):
        newLight = LightFromDatabase(channel,self.lightInformation)
        return newLight



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
        self.channelNames = ["colour","goboRoation","gobo","intensity","pan","tilt","effects"]
        self.channels = ["Colour","Gobo Rotation","Gobo","Intensity","Pan","Tilt","Effects"]
        self.createChannelValues()
    def generateNewLight(self,channel):
        newLight = Miniscan(channel)
        return newLight


class RGB6Channel(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "RGB6Channel"
        self.dropdownName = "RGB 6 Channel Light"
        self.channelNames = ["intensity","red","green","blue","strobe","colourFade"]
        self.channels = ["Intensity","Red","Green","Blue","Strobe","ColourFade"]
        for i in range(len(self.channelNames)):
            if i > 3:
                setattr(self,self.channelNames[i],0)
            else:
                setattr(self,self.channelNames[i],255)
        self.createChannelValues()
    def generateNewLight(self,channel):
        newLight = RGB6Channel(channel)  #where NewLight is the class name but newLight is the variable newLight
        return newLight


class RGB8Channel(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "RGB8Channel"
        self.dropdownName = "RGB 8 Channel Light"
        self.channels = ["Intensity","Red","Green","Blue","White","ColourFader","ColourChooser","Strobe"]
        self.channelNames = ["intensity","red","green","blue","white","colourFader","colourChooser","strobe"]
        for i in range(len(self.channelNames)):
            if i > 3:
                setattr(self,self.channelNames[i],0)
            else:
                setattr(self,self.channelNames[i],255)
        self.createChannelValues()
    def generateNewLight(self,channel):
        newLight = RGB8Channel(channel)  #where NewLight is the class name but newLight is the variable newLight
        return newLight


class RGBLight(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType="RGBLight"
        self.dropdownName = "RGB Light with intensity"
        self.channelNames = ["intensity","red","green","blue"]
        for channel in self.channelNames:
            setattr(self,channel,255)
        self.channels = ["Intensity","Red","Green","Blue"]
        self.createChannelValues()
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
        self.channelNames = ["red","green","blue","white"]
        self.createChannelValues()
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
        self.channelNames = ["intensity"]
        self.createChannelValues()
    def generateNewLight(self,channel):
        newLight = GenericDimmer(channel)
        return newLight

class LEDBar24ChannelMode(Light):
    def __init__(self,startChannel,infoMode = False):
        Light.__init__(self,startChannel,infoMode)
        self.lightType = "LEDBar24ChannelMode"
        self.dropdownName = "LED bar 24 channel mode"
        colours = ["red","green","blue"]
        self.channelNames = []
        for i in range(1,9,1):
            for colour in colours:
                setattr(self,f"{colour}{i}",255)
                self.channelNames.append(f"{colour}{i}")

        coloursCaptialised = ["Red","Green","Blue"]
        self.channels = []
        for i in range(1,9,1):
            for colour in coloursCaptialised:
                self.channels.append(f"{colour}{i}")
        self.createChannelValues()
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
