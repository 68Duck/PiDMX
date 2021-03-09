import serial
import time
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import sys
import threading
import math as maths
import sqlite3 as lite
import random



class DMXOffMode(object): #used when xlr is not connected
    def __init__(self):
        pass
    def send(self):
        # print("dmx is not working")
        pass
    def set_data(self,test="",test2="",test3="",test4="",test5=""):
        pass
