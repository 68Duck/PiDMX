import serial
import time
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import random

class PyDMX:  ##Coppied from the internet. This does the sending to dmx stuff
    def __init__(self,COM='COM8',Brate=250000,Bsize=8,StopB=2):
        #start serial
        self.working = True
        try:
            self.ser = serial.Serial(COM,baudrate=Brate,bytesize=Bsize,stopbits=StopB)
        except:
            self.working = False
            print("The serial is not working. Please make sure the lights are plugged in and that you don't have any other dmx scripts running and make sure the port is correct")
            # while True:
            #     print("Please close and restart the program")
        self.data = np.zeros([513],dtype='uint8')
        self.data[0] = 0 # StartCode
        self.sleepms = 50.0
        self.breakus = 176.0
        self.MABus = 16.0

    def set_random_data(self):
        self.data[1:513]= np.random.rand(512)*255

    def set_data(self,id,data):
        self.data[id]=data

    def send(self):
        # Send Break : 88us - 1s
        self.ser.break_condition = True
        time.sleep(self.breakus/1000000.0)

        # Send MAB : 8us - 1s
        self.ser.break_condition = False
        time.sleep(self.MABus/1000000.0)

        # Send Data
        self.ser.write(bytearray(self.data))

        # Sleep
        time.sleep(self.sleepms/1000.0) # between 0 - 1 sec

    def sendzero(self):
        self.data = np.zeros([513],dtype='uint8')
        self.send()
