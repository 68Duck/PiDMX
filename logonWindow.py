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

from databaseManager import DataBaseManager
from createAccountWindow import CreateAccountWindow
from errorWindow import ErrorWindow
from lightDisplayWindow import LightDisplayWindow

class LogonWindow(QMainWindow,uic.loadUiType("logon.ui")[0]):
    def __init__(self,lightDisplay):
        super().__init__()
        self.setupUi(self)
        self.tabs.setCurrentIndex(0)
        self.lightDisplay = lightDisplay
        self.logonValid = False
        self.logonDatabaseManager = DataBaseManager("logon.db")
        self.setFixedSize(self.size())
        self.initUI()

    def initUI(self):
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
        self.lightDisplay.show()




# class LogonWindow(QWidget):
#     def __init__(self,lightDisplay):
#         super().__init__()
#         self.lightDisplay = lightDisplay
#         self.logonValid = False
#         self.logonDatabaseManager = DataBaseManager("logon.db")
#         self.setGeometry(200,100,500,500)
#         self.setWindowTitle("Log on")
#         self.initUI()
#         self.show()
#
#     def initUI(self):
#         self.usernameInput = QLineEdit(self)
#         self.usernameInput.setPlaceholderText("Enter Username")
#         self.usernameInput.move(50,50)
#
#         self.passwordInput = QLineEdit(self)
#         self.passwordInput.setPlaceholderText("Enter Password")
#         self.passwordInput.move(50,100)
#
#         self.submitButton = QtWidgets.QPushButton(self)
#         self.submitButton.move(50,150)
#         self.submitButton.setText("Submit")
#         self.submitButton.clicked.connect(self.submitButtonPressed)
#
#         self.createAccountButton = QPushButton(self)
#         self.createAccountButton.move(50,200)
#         self.createAccountButton.setText("Create new account")
#         self.createAccountButton.clicked.connect(self.createAccountButtonClicked)
#
#     def keyPressEvent(self,e):
#         if e.key() == Qt.Key_Return:
#             self.submitButtonPressed()
#
#     def createAccountButtonClicked(self):
#         self.createAccountWindow = CreateAccountWindow(self.logonDatabaseManager,self)
#         self.createAccountWindow.show()
#
#     def createDatabase(self,databaseID):
#         self.dataBaseManager = DataBaseManager("dmx"+str(databaseID)+".db")
#         self.dataBaseManager.createLightingRigsTable()
#         self.dataBaseManager.createMainPlaybackTable()
#         self.dataBaseManager.createMainSequenceTable()
#
#     def submitButtonPressed(self):
#         username = self.usernameInput.text()
#         password = self.passwordInput.text()
#         self.logonValid = self.passwordValidation(username,password)
#         if self.logonValid is not False:
#             self.databaseID = self.logonValid
#             if self.databaseID == 0:
#                 self.dataBaseManager = DataBaseManager("dmx.db")
#             else:
#                 self.dataBaseManager = DataBaseManager("dmx"+str(self.databaseID)+".db")
#             self.openLightDisplay()
#         else:
#             self.errorWindow = ErrorWindow("The username or password is not valid. Please try again. Logon is case sensitive")
#             self.usernameInput.setText("")
#             self.passwordInput.setText("")
#
#     def passwordValidation(self,username,password):
#         logons = self.logonDatabaseManager.getAllData("logon")
#         for logon in logons:
#             if logon[1] == username:
#                 if logon[2] == password:
#                     return logon[3]
#         return False
#
#     def openLightDisplay(self):
#         self.lightDisplay = LightDisplayWindow(self.lightDisplay,self.dataBaseManager)
#         self.lightDisplay.show()
