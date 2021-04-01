from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from sortByTerm import sortByTerm
from errorWindow import ErrorWindow
from confirmWindow import ConfirmWindow

class EditSequenceWindow(QWidget,uic.loadUiType("editSequenceWindow.ui")[0]):
    def __init__(self,dataBaseManager,sequenceWindow):
        super().__init__()
        self.setupUi(self)
        self.dataBaseManager = dataBaseManager
        self.sequenceWindow = sequenceWindow
        self.setWindowTitle("Edit Sequence")
        self.removeConfirmed = False
        # self.setGeometry(250,250,300,250)  #x,y,width,height

        self.initUI()
    def initUI(self):
        self.sequenceToOpen = self.dataBaseManager.getAllData("sequence"+str(self.sequenceWindow.sequenceID))
        # layout = QHBoxLayout()
        # self.setLayout(layout)
        self.tableWidget = TableWidget(self)
        self.layout.addWidget(self.tableWidget)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["number","time delay","select"])
        # self.table.hide()
        self.tableWidget.setRowCount(len(self.sequenceToOpen))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        xPos = 0
        yPos = 0
        self.checkBoxes = []
        for i in range(len(self.sequenceToOpen)):
            id = QTableWidgetItem(str(self.sequenceToOpen[i][0]))
            self.tableWidget.setItem(i,0,id)  #in the from x,y,item
            timeDelay = QTableWidgetItem(str(self.sequenceToOpen[i][2]))
            self.tableWidget.setItem(i,1,timeDelay)  #in the from x,y,item
            # self.checkBox = QCheckBox(self)
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxItem.setTextAlignment(Qt.AlignCenter)
            chkBoxItem.setCheckState(Qt.Unchecked)

            self.tableWidget.setItem(i,2,chkBoxItem)
            self.checkBoxes.append(chkBoxItem)

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        self.updateButton.clicked.connect(self.updateButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

    def orderChanged(self):
        for row in range(len(self.sequenceToOpen)):
            rowNumber = QTableWidgetItem(str(row+1))
            self.tableWidget.setItem(row,0,rowNumber)

    def deleteButtonClicked(self):
        self.confirmWindow = ConfirmWindow(self,removePlaybackFromSequence = True)
        if self.removeConfirmed:
            self.removeConfirmed = False
            for row in range(len(self.sequenceToOpen)):
                    itemArray = []
                    for row in range(len(self.sequenceToOpen)):
                        array = []
                        if self.tableWidget.item(row,2).checkState():
                            pass
                        else:
                            for column in range(2):
                                item = self.tableWidget.item(row,column).text()
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
            self.tableWidget.hide()
            self.initUI()
                # print(self.tableWidget.item(row,2).checkState())


    def updateButtonClicked(self):
        itemArray = []
        for row in range(len(self.sequenceToOpen)):
            array = []
            for column in range(2):
                item = self.tableWidget.item(row,column).text()
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


class TableWidget(QTableWidget):  #taken from https://stackoverflow.com/questions/26227885/drag-and-drop-rows-within-qtablewidget
    def __init__(self,parentWindow):
        super().__init__()
        self.parentWindow = parentWindow
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setStyleSheet("background-color:white;")

    def dropEvent(self, event: QDropEvent):
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)
            self.parentWindow.orderChanged()
        super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()
