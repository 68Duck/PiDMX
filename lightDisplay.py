import serial
import time
import numpy as np
import sys
import math as maths
import sqlite3 as lite
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from pydmx import PyDMX
from lightTypes import RGB6Channel,RGBLight,GenericDimmer,LEDBar24ChannelMode,Miniscan
from databaseManager import DataBaseManager
from sshUpdateDatabase import SSHUpdateDatabase
from sshRunFile import SSHRunFile
from logonWindow import LogonWindow
from errorWindow import ErrorWindow

class LightDisplay(QWidget):
    def __init__(self,lights = [],interval = 1,app=None,devMode = False):
        super().__init__()
        self.devMode = devMode
        self.app = app
        self.lights = lights
        self.interval = interval
        self.lightsInformation = [RGBLight(0,True),GenericDimmer(0,True),LEDBar24ChannelMode(0,True),RGB6Channel(0,True),Miniscan(0,True)]
        self.lightTypes = ["GenericDimmer","RGBLight","LEDBar24ChannelMode","RGB6Channel","Miniscan"]
        self.runLoop = True
        self.chaseOn = False
        self.runningChaser = False
        self.runningRainbow = False
        self.raspberryPiDMXMode = False
        self.computerDMXMode = False
        self.dmxOffMode = False
        self.initialiseRainbow()
        self.rainbowChangeAmount = 10
        self.selectedLights = []
        self.displayLock = False
        self.universeLock = False
        self.createBlankUniverse()
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(1)
        self.effectLastRun = time.time()
        self.updateOccupiedChannels()
        self.databaseManager = DataBaseManager("universeValues.db")
        self.password = None
        self.sshUpdateDatabase = SSHUpdateDatabase(self)
        if self.devMode:
            self.sshUpdateDatabase.raspberryPiLoginWindow.hide()
            self.sshUpdateDatabase.runWithoutDMX()

    def runComputerDMX(self):
        self.dmx = PyDMX('COM3')
        if self.dmx.working:
            pass
        else:
            self.errorWindow = ErrorWindow("DMX could not connect. It has been set to DMX OFF mode.")
            print("The program has been set to DMX OFF mode.")
            self.runWithoutDMX()
            return
        self.computerDMXMode = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.runDMX)
        self.timer.start(1)
        self.logonWindow = LogonWindow(self,self.app)
        self.logonWindow.show()

    def runDMX(self):
        if not self.universeLock:
            self.dmx.send()

    def runWithoutDMX(self):
        self.dmxOffMode = True
        self.logonWindow = LogonWindow(self,self.app,devMode=self.devMode)
        if not self.devMode:
            self.logonWindow.show()

    def sshPasswordInputed(self):
        self.raspberryPiDMXMode = True
        self.universeChanged()
        self.sshRunFile = SSHRunFile(password = self.password)
        self.logonWindow = LogonWindow(self,self.app)
        self.logonWindow.show()


    def sendEffectsToLights(self):
        if len(self.selectedLights) > 0:
            if self.runningChaser:
                if self.effectLastRun + (self.selectedLights[0].parentWindow.effectsWindow.chaserDelay) < time.time(): #this could be a source of an error if selectedLights becomes 0 somehow
                    self.effectLastRun = time.time()
                    self.runChase()
                    for displayLight in self.selectedLights:
                        for light in self.lights:
                            if light.startChannel == displayLight.channelNumber:
                                if self.chaseOn:
                                    light.setToBlack()
                                else:
                                    light.setToOrigional()
                                displayLight.changeColourAccordingToFixture()


                if self.runningRainbow:
                    if self.effectLastRun + (self.selectedLights[0].parentWindow.effectsWindow.chaserDelay) < time.time(): #this could be a source of an error if selectedLights becomes 0 somehow
                        self.effectLastRun = time.time()
                        self.runRainbow()
                        for displayLight in self.selectedLights:
                            for light in self.lights:
                                if light.startChannel == displayLight.channelNumber:
                                    update = True
                                    if light.lightType == "RGB6Channel" or light.lightType == "RGBLight":
                                        light.channelValues[1] = self.redRainbow  #red is 1 green is 2 blue is 3 for rgbLight and RGB6Channel
                                        light.channelValues[2] = self.greenRainbow
                                        light.channelValues[3] = self.blueRainbow
                                    elif light.lightType == "LEDBar24ChannelMode":
                                        for i in range(8):
                                            light.channelValues[3*i] = self.redRainbow
                                            light.channelValues[3*i+1] = self.greenRainbow
                                            light.channelValues[3*i+2] = self.blueRainbow

                                    else:
                                        update=False  #probably no way of doing rainbow e.g. in generic dimmer
                                    if update:
                                        light.updateChannelValues()
                                        light.changeUniverse()
                                        finished = displayLight.changeColourAccordingToFixture()




    def universeChanged(self):
        if self.raspberryPiDMXMode:
            self.databaseManager.deleteAllRows("universe")
            records = []
            for i in range(len(self.universeChannelValues)):
                records.append((None,i,self.universeChannelValues[i]))
            self.databaseManager.insertMultipleRecords("universe",records)
            self.sshUpdateDatabase.updateDatabase()
        elif self.computerDMXMode:
            while self.universeLock:
                pass
            if not self.universeLock:
                for i in range(len(self.universeChannelValues)):
                    self.dmx.set_data(int(i),int(self.universeChannelValues[i]))  #should be int(i+1) Dont know why I have done it like this
        elif self.dmxOffMode:
            pass
        else:
            self.errorWindow = ErrorWindow("No dmx mode has been set")


    def createBlankUniverse(self):  ##needed for when closing a rig to open a new one
        self.universeLock = True
        self.universeChannelValues = []
        for i in range(512):
            self.universeChannelValues.append(0)
        self.universeLock = False


    def run(self):
        self.sendEffectsToLights()


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
            # print(self.redRainbow,self.greenRainbow,self.blueRainbow)


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

    def runChase(self):
        if self.chaseOn:
            self.chaseOn = False
        else:
            self.chaseOn = True


    def commitToLights(self,startingChannelNumber,red,green,blue):
        for light in self.lights:
            if light.startChannel == startingChannelNumber:
                light.red = red
                light.green = green
                light.blue = blue

    def commitToChannel(self,channelNumber,channelValue,startingChannelNumber,multipleChannelsChanged=False): #channel number starts at 0
        for light in self.lights:
            if light.startChannel == startingChannelNumber:
                light.channelValues[channelNumber] = channelValue
                # if not multipleChannelsChanged: #this is so if changing multiple channels then can be called only once if needed for performance i.e. not updating database 10 times
                light.updateChannelValues()
                light.changeUniverse(updateUniverse=False)
        if not multipleChannelsChanged:
            self.universeChanged()


    def changeIntensity(self,startingChannelNumber,intensity):
        for light in self.lights:
            if light.startChannel == startingChannelNumber:
                light.intensity = intensity

    def updateOccupiedChannels(self):
        self.channelsOccupied = []
        for i in range(512):
            self.channelsOccupied.append(0)
        for light in self.lights:
            for i in range(len(light.channelValues)):
                self.channelsOccupied[light.startChannel+i-1] = 1
