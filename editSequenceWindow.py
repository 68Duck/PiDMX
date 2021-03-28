from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from sortByTerm import sortByTerm
from errorWindow import ErrorWindow

class EditSequenceWindow(QWidget,uic.loadUiType("editSequenceWindow.ui")[0]):
    def __init__(self,dataBaseManager,sequenceWindow):
        super().__init__()
        self.setupUi(self)
        self.dataBaseManager = dataBaseManager
        self.sequenceWindow = sequenceWindow
        self.setWindowTitle("Edit Sequence")
        # self.setGeometry(250,250,300,250)  #x,y,width,height

        self.sequenceToOpen = self.dataBaseManager.getAllData("sequence"+str(self.sequenceWindow.sequenceID))
        self.initUI()
    def initUI(self):
        # self.updateButton = QPushButton(self)
        # self.updateButton.move(185,220)
        self.updateButton.clicked.connect(self.updateButtonClicked)
        # self.updateButton.setText("Update Sequence")
        # self.updateButton.setFixedWidth(100)

        # self.table = QTableWidget(self)
        self.table.setRowCount(len(self.sequenceToOpen))
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # self.table.setColumnCount(2)
        # self.table.setHorizontalHeaderLabels(["number","time delay"])
        xPos = 0
        yPos = 0
        for i in range(len(self.sequenceToOpen)):
            id = QTableWidgetItem(str(self.sequenceToOpen[i][0]))
            self.table.setItem(i,0,id)  #in the from x,y,item
            timeDelay = QTableWidgetItem(str(self.sequenceToOpen[i][2]))
            # print(self.sequenceToOpen[i][2])
            self.table.setItem(i,1,timeDelay)  #in the from x,y,item

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def updateButtonClicked(self):
        itemArray = []
        for row in range(len(self.sequenceToOpen)):
            array = []
            for column in range(2):
                item = self.table.item(row,column).text()
                try:
                    item = float(item)
                except:
                    self.errorWindow = ErrorWindow("The values need to be numbers. Please try again")
                    return
                array.append(item)
            array.insert(0,row+1)
            itemArray.append(array)
        for i in range(len(itemArray)):
            itemArray[i][0] = i+1
        for arr in itemArray:
            for sequence in self.sequenceToOpen:
                if float(sequence[0]) == float(arr[0]):
                    arr.insert(1,sequence[1])
        itemArray = sortByTerm(itemArray,2)  #so sort by third as 0 indexed
        for arr in itemArray:
            arr.pop(2)
        for i in range(len(itemArray)):
            itemArray[i][0] = i+1
        self.dataBaseManager.createSequenceTable(self.sequenceWindow.sequenceID)  #creates a blank table
        for arr in itemArray:
            record = [None,arr[1],arr[2]]
            self.dataBaseManager.insertRecord("sequence"+str(self.sequenceWindow.sequenceID),record)
        self.close()
