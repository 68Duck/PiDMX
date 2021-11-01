from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os


class HelpWindow(QMainWindow,uic.loadUiType(os.path.join("ui","helpWindow.ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Help")
