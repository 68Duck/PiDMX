from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import sys

class InputWindow(QMessageBox):
    def __init__(self,message,windowTitle="input"):
        self.message = message
        self.windowTitle = windowTitle
        super().__init__()     #use super class
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.windowTitle)
        self.setText(self.message)
        self.setIcon(QMessageBox.Question)

        self.inputBox = QLineEdit(self)
        self.inputBox.move(60,40)
        self.inputBox.setPlaceholderText("Enter here")

        self.inputButton = self.buttonClicked.connect(self.buttonPressed)

        x=self.exec_()

    def buttonPressed(self):
        self.input = self.inputBox.text()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = InputWindow("Enter message input thing test ok")
  try:
      print(ex.input)
  except:
      print("There was no input")
  sys.exit(app.exec_())
