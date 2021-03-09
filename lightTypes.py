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
    def changeUniverse(self):
        if self.lightDisplay == False:
            self.errorWindow = ErrorWindow("ERROR LightDisplay has not been defined")
        else:
            self.lightDisplay.universeLock = True
            for i in range(len(self.channelValues)):
                self.lightDisplay.universeChannelValues[self.startChannel+i] = self.channelValues[i]
            self.lightDisplay.universeLock = False
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
        self.red1 = 255
        self.green1 = 255
        self.blue1 = 255
        self.red2 = 255
        self.green2 = 255
        self.blue2 = 255
        self.red3 = 255
        self.green3 = 255
        self.blue3 = 255
        self.red4 = 255
        self.green4 = 255
        self.blue4 = 255
        self.red5 = 255
        self.green5 = 255
        self.blue5 = 255
        self.red6 = 255
        self.green6 = 255
        self.blue6 = 255
        self.red7 = 255
        self.green7 = 255
        self.blue7 = 255
        self.red8 = 255
        self.green8 = 255
        self.blue8 = 255
        self.channels = ["Red1","Green1","Blue1","Red2","Green2","Blue2","Red3","Green3","Blue3","Red4","Green4","Blue4","Red5","Green5","Blue5","Red6","Green6","Blue6","Red7","Green7","Blue7","Red8","Green8","Blue8"]
        self.channelValues = [self.red1,self.green1,self.blue1,self.red2,self.green2,self.blue2,self.red3,self.green3,self.blue3,self.red4,self.green4,self.blue4,self.red5,self.green5,self.blue5,self.red6,self.green6,self.blue6,self.red7,self.green7,self.blue7,self.red8,self.green8,self.blue8]
        self.previousValues = self.channelValues
    def updateChannelValues(self):
        self.red1 = self.channelValues[0]
        self.green1 = self.channelValues[1]
        self.blue1 = self.channelValues[2]
        self.red2 = self.channelValues[3]
        self.green2 = self.channelValues[4]
        self.blue2 = self.channelValues[5]
        self.red3 = self.channelValues[6]
        self.green3 = self.channelValues[7]
        self.blue3 = self.channelValues[8]
        self.red4 = self.channelValues[9]
        self.green4 = self.channelValues[10]
        self.blue4 = self.channelValues[11]
        self.red5 = self.channelValues[12]
        self.green5 = self.channelValues[13]
        self.blue5 = self.channelValues[14]
        self.red6 = self.channelValues[15]
        self.green6 = self.channelValues[16]
        self.blue6 = self.channelValues[17]
        self.red7 = self.channelValues[18]
        self.green7 = self.channelValues[19]
        self.blue7 = self.channelValues[20]
        self.red8 = self.channelValues[21]
        self.green8 = self.channelValues[22]
        self.blue8 = self.channelValues[23]
    def generateNewLight(self,channel):
        newLight = LEDBar24ChannelMode(channel)
        return newLight
