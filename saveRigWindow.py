from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class SaveRigWindow(QMessageBox):
    def __init__(self,dataBaseManager,lightDisplay,visualLightDisplay,autoSave = False):
        self.autoSave = autoSave
        super().__init__()     #use super class of QMainWindow
        self.dataBaseManager = dataBaseManager
        self.lightDisplay = lightDisplay
        self.visualLightDisplay = visualLightDisplay
        if not self.autoSave:
            self.rigName = False
            self.errorState = False
            self.initUI()
    def initUI(self):   #create UI

        self.setWindowTitle("Save Rig")
        self.setText("Enter the name of the rig that you are saving")
        self.setIcon(QMessageBox.Question)

        self.saveName = QLineEdit(self)      #creates a box where the user can input text
        self.saveName.move(100,40)
        self.saveName.setPlaceholderText("Enter rig name")

        self.saveButton = self.buttonClicked.connect(self.buttonPressed)

        x = self.exec_()
    def buttonPressed(self):
        self.rigName = self.saveName.text()
        nameAlreadyUsed = self.dataBaseManager.checkIfTableNameAlreadyUsed(self.rigName)
        if nameAlreadyUsed:
            self.errorState = True
            self.errorWindow = ErrorWindow("This table name already exixts. Please try again")
        else:
            self.saveRig()

    def getNextRigID(self):
        exisits = True
        counter = 0
        while exisits:
            exisits = self.dataBaseManager.checkIfTableExisits("rig"+str(counter))
            counter += 1
        counter -= 1 #as the last one didn't exist so this is the next one
        return counter

    def saveRig(self):
        newRig = []
        for light in self.visualLightDisplay.lightList:
            newRig.append([None,light.lightType,light.xPos,light.yPos,light.channelNumber])  #null is the primary key so will be done automatically
        try:
            if not self.autoSave:
                self.newRigID = self.getNextRigID()
                self.dataBaseManager.insertRecord("LightingRigs",[None,self.rigName,self.newRigID])
            self.dataBaseManager.createRigTable(self.newRigID)
            for record in newRig:
                self.dataBaseManager.insertRecord("rig"+str(self.newRigID),record)
        except:
            self.errorState = True
            self.errorWindow = ErrorWindow("Data base is not working. Possibly data base is locked?")
