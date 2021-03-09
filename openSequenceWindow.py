from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from errorWindow import ErrorWindow

class OpenSequenceWindow(QWidget):
    def __init__(self,dataBaseManager,sequenceWindow):
        super().__init__()
        self.sequenceWindow = sequenceWindow
        self.dataBaseManager = dataBaseManager
        self.sequenceOpened = False
        self.removeConfirmed = False
        self.setWindowTitle("Open Sequence")
        self.initUI()

    def initUI(self):
        self.openButton = QPushButton(self)
        self.openButton.move(300,200)
        self.openButton.setFixedWidth(100)
        self.openButton.setText("Open")
        self.openButton.clicked.connect(self.openButtonClicked)

        self.deleteButton = QPushButton(self)
        self.deleteButton.move(300,100)
        self.deleteButton.setFixedWidth(100)
        self.deleteButton.setText("Delete Sequence")
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        self.savedSequences = self.dataBaseManager.getAllData("Sequences")

        self.dropDown = QComboBox(self)
        self.dropDown.move(50,50)
        self.dropDown.setMinimumWidth(200)
        for sequence in self.savedSequences:
            if self.sequenceWindow.rigID == sequence[4]:  #checks is the rigID is the same
                self.dropDown.addItem(sequence[2])  #sequence[2] is the name of the sequence

    def deleteButtonClicked(self):
        confirmWindow = ConfirmWindow(self,removeSequence = True)
        if self.removeConfirmed:
            sequenceToDelete = self.dropDown.currentText()
            if sequenceToDelete == "":
                self.errorWindow = ErrorWindow("This sequence does not exisit. Try saving a sequence before trying to delete one.")
            else:
                self.dataBaseManager.deleteSequenceFromSequences(sequenceToDelete)
                for sequence in self.savedSequences:
                    if sequenceToDelete == sequence[2]:
                        sequenceID = sequence[1]
                        sequenceCreatorID = sequence[3]
                self.dataBaseManager.dropSequenceTable(sequenceID)
                self.dataBaseManager.dropSequenceCreatorTable(sequenceCreatorID)
            self.close()

    def openButtonClicked(self):
        self.sequence = self.dropDown.currentText()
        self.sequenceCreatorID = False
        for sequence in self.savedSequences:
            if self.sequence == sequence[2]:
                self.sequenceCreatorID = sequence[3]
                self.sequenceID = sequence[1]
        if self.sequenceCreatorID == False and self.sequenceCreatorID != 0:
            self.sequenceOpened = False
            self.errorWindow = ErrorWindow("This rig does not exist. Try saving a rig first")
        else:
            self.sequenceToOpen = self.dataBaseManager.getAllData("sequenceCreator"+str(self.sequenceCreatorID))
            if self.sequenceToOpen == False:
                self.errorWindow = ErrorWindow("The sequence you have selected does not exist. Please try again")
            else:
                self.closeSequence()
                self.openSequence()
                self.sequenceOpened = True

        self.close()

    def closeSequence(self):
        self.sequenceWindow.lightsToPlace = self.sequenceWindow.lights[:] #[:] creates a copy so the lists dont interact with each other
        for light in self.sequenceWindow.displayLights:
            light.remove()

    def closeEvent(self,*args,**kargs):
        if self.sequenceOpened:
            self.sequenceWindow.openWindowClosed()

    def openSequence(self):
        if self.sequenceToOpen == False:
            self.errorWindow = ErrorWindow("The sequence you have selected does not exist. Please try again")
        else:
            for light in self.sequenceToOpen:
                lightName = light[1]
                lightType = light[2]
                xPos = light[3]
                yPos = light[4]
                self.sequenceWindow.createLight(lightType,lightName,xPos,yPos,openFromSavedSequence=True)
                lightsAlreadyPlaced = []
                for l in self.sequenceWindow.lightsToPlace:
                    if lightName == l.lightType+""+str(l.channelNumber):
                        lightsAlreadyPlaced.append(l)
                for l in lightsAlreadyPlaced:
                    self.sequenceWindow.lightsToPlace.remove(l)
