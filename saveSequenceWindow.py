from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from errorWindow import ErrorWindow

class SaveSequenceWindow(QMessageBox):
    def __init__(self,dataBaseManager,sequenceWindow,autoSave = False):
        self.autoSave = autoSave
        super().__init__()     #use super class of QMainWindow
        self.dataBaseManager = dataBaseManager
        self.sequenceWindow = sequenceWindow
        if not self.autoSave:
            self.sequenceName = False
            self.errorState = False
            self.initUI()
    def initUI(self):   #create UI

        self.setWindowTitle("Save Sequence")
        self.setText("Enter the name of the sequence that you are saving")
        self.setIcon(QMessageBox.Question)

        self.saveName = QLineEdit(self)      #creates a box where the user can input text
        self.saveName.move(100,40)
        self.saveName.setPlaceholderText("Enter sequence name")

        self.saveButton = self.buttonClicked.connect(self.buttonPressed)

        x = self.exec_()
    def buttonPressed(self):
        self.sequenceName = self.saveName.text()
        nameAlreadyUsed = self.dataBaseManager.checkIfSequenceTableNameExists(self.sequenceName)
        if nameAlreadyUsed:
            self.errorState = True
            self.errorWindow = ErrorWindow("This table name already exixts. Please try again")
        else:
            self.saveSequenceCreator()
            self.saveSequence()

    def getNextSequenceID(self):
        exisits = True
        counter = 0
        while exisits:
            exisits = self.dataBaseManager.checkIfTableExisits("sequence"+str(counter))
            counter += 1
        counter -= 1 #as the last one didn't exist so this is the next one
        return counter

    def getNextSequenceCreatorID(self):
        exisits = True
        counter = 0
        while exisits:
            exisits = self.dataBaseManager.checkIfTableExisits("sequenceCreator"+str(counter))
            counter += 1
        counter -= 1 #as the last one didn't exist so this is the next one
        return counter

    def saveSequenceCreator(self):
        newSequenceCreator = []
        for light in self.sequenceWindow.displayLights:
            newSequenceCreator.append([None,light.lightName,light.lightType,light.xPos,light.yPos])
        try:
            if not self.autoSave:
                self.newSequenceCreatorID = self.getNextSequenceCreatorID()
            self.dataBaseManager.createSequenceCreatorTable(self.newSequenceCreatorID)
            for record in newSequenceCreator:
                self.dataBaseManager.insertRecord("sequenceCreator"+str(self.newSequenceCreatorID),record)
        except:
            self.errorState = True
            self.errorWindow = ErrorWindow("Data base is not working. Possibly data base is locked?")

    def saveSequence(self):
        newSequence = []
        for playback in self.sequenceWindow.playbacks:
            newSequence.append([None,playback[0],playback[1]]) #playback[0] is the ID, playback[1] is the timedelay
        try:
            if not self.autoSave:
                self.newSequenceID = self.getNextSequenceID()
                self.dataBaseManager.insertRecord("Sequences",[None,self.newSequenceID,self.sequenceName,self.newSequenceCreatorID,self.sequenceWindow.rigID])
            self.dataBaseManager.createSequenceTable(self.newSequenceID)
            for record in newSequence:
                self.dataBaseManager.insertRecord("sequence"+str(self.newSequenceID),record)
        except:
            self.errorState = True
            self.errorWindow = ErrorWindow("Data base is not working. Possibly data base is locked?")
