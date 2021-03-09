from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class ErrorWindow(QMessageBox):
    def __init__(self,message):
        super(ErrorWindow,self).__init__()     #use super class of QMainWindow
        self.message = message
        self.initUI()
    def initUI(self):   #create UI

        self.setWindowTitle("Error")
        self.setText(self.message)
        self.setIcon(QMessageBox.Critical)

        x = self.exec_()
