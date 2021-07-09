from PyQt5 import QtCore,uic
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel
# from PyQt5.QtGui import Qt
from PyQt5.QtCore import QEvent,Qt
import sys
import os

from databaseManager import DataBaseManager
from messageWindow import MessageWindow
from errorWindow import ErrorWindow
from confirmWindow import ConfirmWindow
from inputWindow import InputWindow
from barClass import Bar

class BarsEditWindow(QMainWindow,uic.loadUiType(os.path.join("ui","BarsEditWindow.ui"))[0]):
    def __init__(self,app):
        super(QMainWindow).__init__()
        super(uic.loadUiType(os.path.join("ui","BarsEditWindow.ui"))[0]).__init__()
        super().__init__()
        self.setMouseTracking(True)
        self.dataBaseManager = DataBaseManager("bars.db")
        self.setupUi(self)
        self.setWindowTitle("Bars Edit Window")
        self.initUI()
        app.installEventFilter(self)
        self.show()

    def initUI(self):
        self.previousBarLocation = None
        self.bars = []
        self.squareParts = []
        self.tempBar = None
        self.movingPoint = None
        self.movingBar = None
        self.tempSquares = []
        self.currentBarLetter = None
        self.creatingHorizontalBar = False
        self.creatingVerticalBar = False
        self.creatingInitialSquarePoint = False
        self.creatingFinalSquarePoint = False
        self.changingBarSize = False
        self.menuAdd_new_bar.setEnabled(False)
        self.actionAddStageSquare.setEnabled(False)
        self.submitButton.clicked.connect(self.submitButtonPressed)
        self.openButton.clicked.connect(self.openButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.actionHorizontal.triggered.connect(self.createHorizontalBar)
        self.actionVertical.triggered.connect(self.createVerticalBar)
        self.actionOpen_location.triggered.connect(self.openWidget)
        self.actionAddStageSquare.triggered.connect(self.actionAddStageSquareClicked)
        self.changeBarSizeButton.triggered.connect(self.changeBarSizeButtonClicked)
        self.changeBarSizeButtonClicked()
        self.locations = self.dataBaseManager.getAllData("locations")
        for location in self.locations:
            self.openDropDown.addItem(location["locationName"])

        self.creatingSquareLabel.hide()
        self.creatingSquareLabel_2.hide()

    def changeBarSizeButtonClicked(self):
        self.changingBarSize = self.changeBarSizeButton.isChecked()

    def getLetterInput(self):
        try:
            self.inputWindow = InputWindow("Enter the letter of the bar","Enter Bar Letter")
            inp = self.inputWindow.input
            if len(inp) != 1:
                raise Exception("Invalid Input")
            else:
                inp = inp.upper()
                if ord(inp) <65 or ord(inp) > 90:
                    raise Exception("The input was not a capital letter")
            return inp
        except:
            self.errorWindow = ErrorWindow("The input was invalid. Please try again")
            return False

    def createHorizontalBar(self):
        inp = self.getLetterInput()
        if inp is False:
            pass
        else:
            self.creatingHorizontalBar = True
            self.currentBarLetter = inp

    def createVerticalBar(self):
        inp = self.getLetterInput()
        if inp is False:
            pass
        else:
            self.creatingVerticalBar = True
            self.currentBarLetter = inp

    def createSquareSide(self,x,y,width,height):
        self.side = QLabel(self)
        self.side.move(x,y)
        self.side.setFixedSize(width,height)
        self.side.setStyleSheet("background-color:white")
        self.side.show()
        return self.side

    def drawTempSquare(self,firstPoint,secondPoint):
        x,y = firstPoint
        x1,y1 = secondPoint
        self.x0,self.y0 = firstPoint
        self.x1,self.y1 = secondPoint
        width = abs(x1-x)
        height = abs(y1-y)
        sx = True if x<x1 else False
        sy = True if y<y1 else False
        sideWidth = 5

        for label in self.tempSquares:
            label.hide()
        self.tempSquareL = self.createSquareSide(x if sx else x1,y if sy else y1,sideWidth,height)
        self.tempSquareT = self.createSquareSide(x if sx else x1,y if sy else y1,width,sideWidth)
        self.tempSquareR = self.createSquareSide(x1 if sx else x,y if sy else y1,sideWidth,height+5)
        self.tempSquareB = self.createSquareSide(x if sx else x1,y1 if sy else y,width,sideWidth)
        self.tempSquares = [self.tempSquareL,self.tempSquareR,self.tempSquareT,self.tempSquareB]

    def createSquare(self):
        if len(self.tempSquares) > 0:
            self.s0,self.s1,self.s2,self.s3 = self.tempSquares
            self.squareParts.append(self.s0)
            self.squareParts.append(self.s1)
            self.squareParts.append(self.s2)
            self.squareParts.append(self.s3)
            record = (None,self.x0,self.y0,self.x1,self.y1)
            self.dataBaseManager.insertRecord(self.squaresTableName,record)
            self.tempSquares = []
            return True
        else:
            return False

    def createSquareFromDatabase(self,square):
        firstPoint = (square["x0"],square["y0"])
        secondPoint = (square["x1"],square["y1"])
        x,y = firstPoint
        x1,y1 = secondPoint
        width = abs(x1-x)
        height = abs(y1-y)
        sx = True if x<x1 else False
        sy = True if y<y1 else False
        sideWidth = 5
        self.sL = self.createSquareSide(x if sx else x1,y if sy else y1,sideWidth,height)
        self.sT = self.createSquareSide(x if sx else x1,y if sy else y1,width,sideWidth)
        self.sR = self.createSquareSide(x1 if sx else x,y if sy else y1,sideWidth,height+5)
        self.sB = self.createSquareSide(x if sx else x1,y1 if sy else y,width,sideWidth)
        self.sides = [self.sL,self.sT,self.sR,self.sB]
        for side in self.sides:
            self.squareParts.append(side)


    # def mouseMoveEvent(self,e):   #FIX ME
    #     if e.buttons() == Qt.LeftButton:
    #         if not self.movingPoint:
    #             for bar in self.bars:
    #                 if bar.selected:
    #                     for point in bar.points:
    #                         if point.checkIfInRange(e.x(),e.y()):
    #                             self.movingPoint = point
    #                     if not self.movingPoint:
    #                         if bar.checkIfInRange(e.x(),e.y()):
    #                             self.movingBar = bar  #FINISH ME
    #         else:
    #             self.movingPoint.setPosition(e.x(),e.y())
    #     else:
    #         self.movingPoint = None

    def eventFilter(self,source,event):
        if event.type() == QEvent.MouseButtonRelease:
            self.movingPoint = None
            self.movingBar = False
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() == Qt.LeftButton:
                selected = False
                if not self.movingPoint:
                    for bar in self.bars:
                        if bar.selected:
                            for point in bar.points:
                                if point.checkIfInRange(event.x(),event.y()):
                                    self.movingPoint = point
                                    selected = True
                            if not self.movingPoint:
                                if bar.checkIfInRange(event.x(),event.y()):
                                    self.movingBar = bar  #FINISH ME
                                    self.previousBarLocation = (event.x(),event.y()) #moves relative to the current location of the mouse
                                    selected = True
                if not selected:
                    for bar in self.bars:
                        bar.setSelected(False)
        if event.type() == QEvent.MouseMove:
            if event.x() != 0 and event.y() != 0:
                if self.movingPoint:
                        self.movingPoint.setPosition(event.x(),event.y())
                if self.movingBar:
                    dx = event.x() - self.previousBarLocation[0]
                    dy = event.y() - self.previousBarLocation[1]
                    x = self.movingBar.pos[0] + dx
                    y = self.movingBar.pos[1] + dy
                    self.movingBar.setPosition((x,y))
                    self.previousBarLocation = (event.x(),event.y())

        if self.changingBarSize:
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() == Qt.LeftButton:
                    for bar in self.bars:
                        if bar.checkIfInRange(event.x(),event.y()):
                            bar.setSelected(not bar.selected)
        if self.creatingInitialSquarePoint:
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() == Qt.LeftButton:
                    self.initialSquareX = event.x()
                    self.initialSquareY = event.y()
                    self.creatingInitialSquarePoint = False
                    self.creatingFinalSquarePoint = True
                    self.creatingSquareLabel.hide()
                    self.creatingSquareLabel_2.show()
        if self.creatingFinalSquarePoint:
            if event.type() == QEvent.MouseMove:
                self.x = event.x()
                self.y = event.y()
                if self.x != 0 and self.y != 0: #gets rid of the random 0's that appear for some reason
                    self.drawTempSquare((self.initialSquareX,self.initialSquareY),(self.x,self.y))
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() == Qt.LeftButton:
                    self.x = event.x()
                    self.y = event.y()
                    valid = self.createSquare()
                    if valid:
                        self.creatingFinalSquarePoint = False
                        self.creatingSquareLabel_2.hide()
        if self.creatingHorizontalBar or self.creatingVerticalBar:
            if event.type() == QEvent.MouseMove:
                self.x = event.x()
                self.y = event.y()
                if self.x != 0 and self.y != 0: #gets rid of the random 0's that appear for some reason
                    if self.currentBarLetter is not False:
                        self.previewBar(self.x,self.y,self.currentBarLetter,horizontal = True if self.creatingHorizontalBar else False)
                    else:
                        self.errorWindow = ErrorWindow("The bar letter is invalid. Please try again")
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() == Qt.LeftButton:
                    self.x = event.x()
                    self.y = event.y()
                    self.createBar()
                    self.creatingHorizontalBar = False
                    self.creatingVerticalBar = False
        return super(BarsEditWindow, self).eventFilter(source, event)

    def previewBar(self,x,y,barName,horizontal):
        if self.tempBar is not None:
            self.tempBar.hide()
        if horizontal:
            self.tempBar = Bar(barName,x,y,900,25,horizontal,self)
        else:
            self.tempBar = Bar(barName,x,y,25,400,horizontal,self)
        self.tempBar.show()

    def createBarFromDatabase(self,bar):
        barName = bar["barName"]
        width = bar["width"]
        height = bar["height"]
        xPos = bar["xPos"]
        yPos = bar["yPos"]
        horizontal = True if bar["isHorizontal"] else False
        self.newBar = Bar(barName,xPos,yPos,width,height,horizontal,self)
        self.newBar.show()
        self.bars.append(self.newBar)

    def createBar(self):
        if self.tempBar is not None:
            self.bars.append(self.tempBar)
            self.tempBar = None
        self.dataBaseManager.deleteAllRows(self.barTableName)
        for bar in self.bars:
            x,y = bar.pos
            record = (None,1 if bar.width>bar.height else 0,bar.width,bar.height,bar.name,x,y)
            self.dataBaseManager.insertRecord(self.barTableName,record)


    def actionAddStageSquareClicked(self):
        self.creatingSquareLabel.show()
        self.creatingInitialSquarePoint = True

    def submitButtonPressed(self):
        self.tableName = self.newNameInput.text()
        if self.dataBaseManager.checkIfTableExisits(self.tableName):
            self.errorWindow = ErrorWindow("There is already a location with that name. Please try again")
            return
        if self.hasSpaces(self.tableName) or self.tableName == "":
            self.errorWindow = ErrorWindow("The table has numbers or spaces in it. Please try again")
            return
        self.barTableName = f"{self.tableName}Bars"
        self.squaresTableName = f"{self.tableName}Squares"
        self.dataBaseManager.createBarsTable(self.barTableName)
        self.dataBaseManager.createSquaresTable(self.squaresTableName)
        record = [None,self.tableName,self.barTableName,self.squaresTableName]#none is for the id
        self.dataBaseManager.insertRecord("locations",record)
        self.messageWindow = MessageWindow(f"A rig with the name {self.tableName} was created")
        self.setWindowTitle(self.tableName)
        self.closeWidget()


    def openButtonClicked(self):
        location = self.openDropDown.currentText()
        for l in self.locations:
            if l["locationName"] == location:
                barTable = l["barsTableName"]
                squaresTableName = l["squaresTableName"]
        self.barTableName = barTable
        self.squaresTableName = squaresTableName
        bars = self.dataBaseManager.getAllData(self.barTableName)
        squares = self.dataBaseManager.getAllData(self.squaresTableName)
        for bar in bars:
            self.createBarFromDatabase(bar)
        for square in squares:
            self.createSquareFromDatabase(square)
        self.closeWidget()

    def deleteButtonClicked(self):
        location = self.openDropDown.currentText()
        if location == "":
            self.errorWindow = ErrorWindow("There are no locations to delete")
            return
        self.confirmWindow = ConfirmWindow(self,f"Are you sure you want to delete the location {location}?")
        if self.removeConfirmed:
            for l in self.locations:
                if l["locationName"] == location:
                    barTable = l["barsTableName"]
                    squareTable = l["squaresTableName"]
            self.dataBaseManager.deleteBarsAndSquaresTable(barTable,squareTable) #this deletes the table and removes the row from locations
            self.openDropDown.removeItem(0) #removes the first item so the item that is being deleted
        else:
            return

    def closeWidget(self):
        self.menuAdd_new_bar.setEnabled(True)
        self.actionAddStageSquare.setEnabled(True)
        self.widget.hide()

    def openWidget(self):
        for bar in self.bars:
            bar.hide()
        for part in self.squareParts:
            part.hide()
        self.bars = []
        self.openDropDown.clear()
        self.locations = self.dataBaseManager.getAllData("locations")
        for location in self.locations:
            self.openDropDown.addItem(location["locationName"])
        self.menuAdd_new_bar.setEnabled(False)
        self.widget.show()


    def hasSpaces(self,inputString):
        return any(char == " " for char in inputString)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BarsEditWindow(app)
    # app.installEventFilter(win)
    # win.installEventFilter(win)
    sys.exit(app.exec_())
