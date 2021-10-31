import serial
import time
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import random
#
# class PyDMX:  ##Coppied from the internet. This does the sending to dmx stuff
#     def __init__(self,COM='COM8',Brate=250000,Bsize=8,StopB=2):
#         #start serial
#         self.working = True
#         try:
#             self.ser = serial.Serial(COM,baudrate=Brate,bytesize=Bsize,stopbits=StopB)
#         except:
#             self.working = False
#             print("The serial is not working. Please make sure the lights are plugged in and that you don't have any other dmx scripts running and make sure the port is correct")
#             # while True:
#             #     print("Please close and restart the program")
#         self.data = np.zeros([513],dtype='uint8')
#         self.data[0] = 0 # StartCode
#         self.sleepms = 50.0
#         self.breakus = 176.0
#         self.MABus = 16.0
#
#     def set_random_data(self):
#         self.data[1:513]= np.random.rand(512)*255
#
#     def set_data(self,id,data):
#         self.data[id]=data
#
#     def send(self):
#         # Send Break : 88us - 1s
#         self.ser.break_condition = True
#         time.sleep(self.breakus/1000000.0)
#
#         # Send MAB : 8us - 1s
#         self.ser.break_condition = False
#         time.sleep(self.MABus/1000000.0)
#
#         # Send Data
#         self.ser.write(bytearray(self.data))
#
#         # Sleep
#         time.sleep(self.sleepms/1000.0) # between 0 - 1 sec
#
#     def sendzero(self):
#         self.data = np.zeros([513],dtype='uint8')
#         self.send()


class PyDMX(object):
    def __init__(self,port="COM3"):
        self.universeData = [0]*512  #the first item is the start bit so should not change
        baudrate = 250000
        try:
            self.ser = serial.Serial(port,baudrate,bytesize=8,stopbits=2)
            self.working = True
        except Exception as e:
            # print(e)
            self.working = False
            raise Exception("The serial is not working. Please make sure the lights are plugged in and that you don't have any other dmx scripts running and make sure the port is correct")


    def set_data(self,id,data):
        if isinstance(id,float):
            raise Exception("The id needs to be an integer.")
            return
        try:
            id = int(id)
        except:
            raise Exception("The id is not an integer. Please try again")
            return
        if id>512 or id<1:
            raise Exception("The id value needs to be between 1 and 512 inclusive.")
            return
        self.universeData[id] = data

    def send(self,universeData = None):
        if universeData is None:
            pass
        else:
            self.universeData = universeData
        self.ser.send_break(duration=92/1000000)
        time.sleep(12/1000000.0)
        try:
            self.ser.write(0)
            self.ser.write(bytearray(self.universeData))
        except:
            self.ser.close()
            raise Exception("The serial cannot write. Check the cable is plugged in.")
        time.sleep(10/1000)

    def send_zero(self):
        universeData = [0]*1025
        self.send(universeData)

    def send_full(self):
        universeData = [255]*1025
        self.send(universeData)
