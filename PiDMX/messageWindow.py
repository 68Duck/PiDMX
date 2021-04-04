from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class MessageWindow(QMessageBox):
    def __init__(self,message):
        super(MessageWindow,self).__init__()     #use super class of QMainWindow
        self.message = message
        self.initUI()
    def initUI(self):   #create UI

        self.setWindowTitle("Message")
        self.setText(self.message)
        self.setIcon(QMessageBox.Information)

        x = self.exec_()
