import serial
import time
import numpy as np
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import sys
import threading
import math as maths
import sqlite3 as lite
import random
import os

from databaseManager import DataBaseManager
from createAccountWindow import CreateAccountWindow
from errorWindow import ErrorWindow
from lightDisplayWindow import LightDisplayWindow

class LogonWindow(QMainWindow,uic.loadUiType(os.path.join("ui","logon.ui"))[0]):
    def __init__(self,lightDisplay,app,devMode=False):
        super().__init__()
        self.app = app
        self.devMode = devMode
        self.lightDisplay = lightDisplay
        if not self.devMode:
            self.setupUi(self)
            self.tabs.setCurrentIndex(0)
            self.logonValid = False
            self.logonDatabaseManager = DataBaseManager("logon.db")
            self.setFixedSize(self.size())
            self.initUI()
        else:
            self.dataBaseManager = DataBaseManager("dmx.db")
            self.openLightDisplay()

    def initUI(self):
        self.usernameInput.setPlaceholderText("Username")
        self.passwordInput.setPlaceholderText("Password")
        self.createUsernameInput.setPlaceholderText("New Username")
        self.createPasswordInput.setPlaceholderText("New Password")
        self.createPasswordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.submitButton.clicked.connect(self.submitButtonPressed)
        self.submitAccountButton.clicked.connect(self.createAccountButtonClicked)

    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Return:
            self.submitButtonPressed()

    def createAccountButtonClicked(self):
        username = self.createUsernameInput.text()
        password = self.createPasswordInput.text()
        logons = self.logonDatabaseManager.getAllData("logon")
        invalid = False
        for logon in logons:
            if username == logon[1]:
                invalid = True

        if username == "" or password == "":
            self.errorWindow = ErrorWindow("The new username or password is invalid. Please make sure you input some form of data.")
        elif invalid:
            self.errorWindow = ErrorWindow("The username is already taken. Please enter a different username")
        else:

            exists = True
            counter = 0
            while exists:
                exists = False
                for logon in logons:
                    if counter == logon[3]:
                        exists = True
                if not exists:
                    break
                else:
                    counter += 1

            self.newDatabaseId = counter

            self.logonDatabaseManager.insertRecord("logon",[None,username,password,self.newDatabaseId])
            self.createDatabase(self.newDatabaseId)
            self.tabs.setCurrentIndex(0)

            #Alert account created

    def createDatabase(self,databaseID):
        self.dataBaseManager = DataBaseManager("dmx"+str(databaseID)+".db")
        self.dataBaseManager.createLightingRigsTable()
        self.dataBaseManager.createMainPlaybackTable()
        self.dataBaseManager.createMainSequenceTable()

    def submitButtonPressed(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        self.logonValid = self.passwordValidation(username,password)
        if self.logonValid is not False:
            self.databaseID = self.logonValid
            if self.databaseID == 0:
                self.dataBaseManager = DataBaseManager("dmx.db")
            else:
                self.dataBaseManager = DataBaseManager("dmx"+str(self.databaseID)+".db")
            self.openLightDisplay()
        else:
            self.errorWindow = ErrorWindow("The username or password is not valid. Please try again. Logon is case sensitive")
            self.usernameInput.setText("")
            self.passwordInput.setText("")

    def passwordValidation(self,username,password):
        logons = self.logonDatabaseManager.getAllData("logon")
        for logon in logons:
            if logon[1] == username:
                if logon[2] == password:
                    return logon[3]
        return False

    def openLightDisplay(self):
        self.lightDisplay = LightDisplayWindow(self.lightDisplay,self.dataBaseManager)
        self.app.installEventFilter(self.lightDisplay)
        self.lightDisplay.show()
