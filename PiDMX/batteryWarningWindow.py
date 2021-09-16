from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class BatteryWarningWindow(QMessageBox):
    def __init__(self,batteryPercentage):
        super(BatteryWarningWindow,self).__init__()     #use super class of QMainWindow
        self.batteryPercentage = batteryPercentage
        self.initUI()
    def initUI(self):   #create UI

        self.setWindowTitle("Battery Warning")
        self.setText(f"Your battery percentage is {self.batteryPercentage}%. You may want to think about plugging in your device")
        self.setIcon(QMessageBox.Warning)

        x = self.exec_()
