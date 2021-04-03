from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*


class CreateAccountWindow(QWidget):
    def __init__(self,logonDatabaseManager,parentWindow):
        super().__init__()
        self.logonDatabaseManager = logonDatabaseManager
        self.parentWindow = parentWindow
        self.setGeometry(200,100,500,500)
        self.setWindowTitle("Create Account")
        self.initUI()
        self.show()

    def initUI(self):
        self.usernameInput = QLineEdit(self)
        self.usernameInput.setPlaceholderText("Enter New Username")
        self.usernameInput.move(50,50)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setPlaceholderText("Enter New Password")
        self.passwordInput.move(50,100)

        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.move(50,150)
        self.submitButton.setText("Submit")
        self.submitButton.clicked.connect(self.submitButtonPressed)

    def submitButtonPressed(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
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
            self.parentWindow.createDatabase(self.newDatabaseId)
            self.close()
