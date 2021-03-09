from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*


class ConfirmWindow(QMessageBox):  #creates a class window
    def __init__(self,parentWindow,removeRig = False,playbackOveride = False,removePlayback=False,removeSequence = False):
        super().__init__()     #use super class of QMainWindow
        self.parentWindow = parentWindow
        self.removePlayback = removePlayback
        self.removeRig = removeRig
        self.playbackOveride = playbackOveride
        self.removeSequence = removeSequence
        self.initUI()
    def initUI(self):   #create UI

        self.setWindowTitle("Alert!")
        if self.removeRig:
            self.setText("Are you sure you want to remove this rig?")
        elif self.playbackOveride:
            self.setText("This name already exisists. Do you want to overide it.")
        elif self.removePlayback:
            self.setText("Are you sure you want to remove this playback?")
        elif self.removeSequence:
            self.setText("Are you sure you want to remove this sequence?")
        else:
            self.setText("Are you sure you want to remove this light?")
        self.setIcon(QMessageBox.Question)

        self.confirm = self.buttonClicked.connect(self.confirmClicked)

        self.cancelButton = QPushButton(self)
        self.cancelButton.clicked.connect(self.cancelClicked)
        self.cancelButton.setText("Cancel")
        self.cancelButton.move(140,60)
        self.cancelButton.resize(75,20)

        x = self.exec_()

    def confirmClicked(self):
        self.parentWindow.removeConfirmed = True
        self.close()

    def cancelClicked(self):
        self.parentWindow.removeConfirmed = False
        self.close()
