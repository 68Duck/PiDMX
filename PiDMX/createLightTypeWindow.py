from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os

from confirmWindow import ConfirmWindow
from errorWindow import ErrorWindow
from createSpriteWindow import CreateSpriteWindow
from databaseManager import DataBaseManager

class CreateLightTypeWindow(QWidget,uic.loadUiType(os.path.join("ui","CreateLightTypeWindow.ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Create Light Type")
        self.lightName = "none"
        self.imageName = None
        self.dataBaseManager = DataBaseManager("lightTypes.db")
        self.addChannelButton.clicked.connect(self.addChannelButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.createLightButton.clicked.connect(self.createLightButtonClicked)
        self.rgbRadio.clicked.connect(self.radioChanged)
        self.intensityRadio.clicked.connect(self.radioChanged)
        self.createSpriteButton.clicked.connect(self.createSpriteButtonClicked)
        self.panTiltCheckBox.clicked.connect(self.panTiltChanged)
        self.table = TableWidget(self)
        self.layout.addWidget(self.table)
        self.table.itemChanged.connect(self.itemChanged)
        self.checkBoxes = []
        self.indicators = []
        self.removeConfirmed = False
        self.initUI()

    def initUI(self):
        self.rgbRadio.setChecked(True)
        self.radioChanged()
        self.panTiltChanged()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["channel name","channel start value","select"])
        self.table.setRowCount(0)
        header = self.table.horizontalHeader()
        for i in range(2):
            header.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)


    def createSpriteButtonClicked(self):
        self.createSpriteWindow = CreateSpriteWindow(self.lightName,self)
        self.createSpriteWindow.show()

    def hasDuplicates(self,array):
        return len(array) != len(set(array))


    def createLightButtonClicked(self):
        hasPanTilt = self.panTiltCheckBox.isChecked()
        channelNames = []
        for i in range(self.table.rowCount()):
            channelNames.append(self.table.item(i,0).text())
        if self.hasDuplicates(channelNames):
            self.errorWindow = ErrorWindow("You cannot have channels with the same name. Please try again")
            return

        self.lightName = self.lightNameInput.text()
        if self.lightName == "":
            self.errorWindow = ErrorWindow("Please enter a name for the light type")
            return
        elif self.lightName == "none":
            self.errorWindow = ErrorWindow("The light cannot have the name 'none'. Please try a differnet name")
            return
        else:
            lightTypes = self.dataBaseManager.getAllData("lightTypes")
            for light in lightTypes:
                lightName = light[1]
                if self.lightName == lightName:
                    self.errorWindow = ErrorWindow("There is already a light with that name. Please choose a different name")
                    return
        if self.imageName is None:
            self.errorWindow = ErrorWindow("Please create a sprite before saving the image.")
            return
        else:
            newImageName = f"{self.lightName}.png"
            os.rename(os.path.join("images",self.imageName),os.path.join("images",newImageName)) #changes the image name to the name of the light
            self.imageName = newImageName
        if self.rgbRadio.isChecked():
            isRGB = True
            colours = ["red","green","blue","pan","tilt"]
            rgbNames = []
            for colour in colours:
                attr = getattr(self,f"{colour}ChannelInput")
                rgbName = attr.currentText()
                print(rgbName)
                if rgbName != "": #stops not working with pan/tilt if does not exist
                    rgbNames.append(rgbName)
            if self.hasDuplicates(rgbNames):
                self.errorWindow = ErrorWindow("You cannot have the red, green or blue channels with the same name. Please try again")
                return

        if self.intensityRadio.isChecked():
            isRGB = False


        channelID = self.getNextTableID("channels")
        self.dataBaseManager.createChannelsTable(channelID)
        for i in range(self.table.rowCount()):
            channelName = self.table.item(i,0).text()
            startChannelValue = self.table.item(i,1).text()
            channelInformation = None
            if isRGB:
                colours = ["red","green","blue"]
            else:
                colours = ["intensity"]
            if hasPanTilt:
                colours.append("pan")
                colours.append("tilt")
            for colour in colours:
                attr = getattr(self,f"{colour}ChannelInput")
                if attr.currentText() == channelName:
                    channelInformation = colour

            record = [None,channelName,startChannelValue,channelInformation]
            self.dataBaseManager.insertRecord("channels"+str(channelID),record)

        indicatorsID = self.getNextTableID("indicators")
        self.dataBaseManager.createIndicatorsTable(indicatorsID)
        for i in range(len(self.indicators)):
            indicator = self.indicators[i]
            x = indicator.x()
            y = indicator.y()
            width = indicator.width()
            height = indicator.height()
            type = indicator.type
            record = [None,x,y,width,height,type]
            self.dataBaseManager.insertRecord("indicators"+str(indicatorsID),record)


        record = [None,self.lightName,self.imageName,isRGB,hasPanTilt,indicatorsID,channelID]  #needs to have indicators and channel names in new tables
        self.dataBaseManager.insertRecord("lightTypes",record)
        self.close()


    def getNextTableID(self,tableName):
        exisits = True
        counter = 0
        while exisits:
            exisits = self.dataBaseManager.checkIfTableExisits(tableName+str(counter))
            counter += 1
        counter -= 1 #as the last one didn't exist so this is the next one
        return counter


    def radioChanged(self):
        if self.rgbRadio.isChecked():
            self.rgbWidget.show()
            self.intensityWidget.hide()
        else: #so intensity radio
            self.intensityWidget.show()
            self.rgbWidget.hide()
        self.updateChannelDropdowns()

    def panTiltChanged(self):
        if self.panTiltCheckBox.isChecked():
            self.panTiltWidget.show()
        else:
            self.panTiltWidget.hide()
        self.updateChannelDropdowns()

    def itemChanged(self,item):
        row = item.row()
        column = item.column()
        if column == 1:
            text = self.table.item(row,column).text()
            valid = False
            try:
                text = int(text)
                if text > 255:
                    text = 255
                elif text < 0:
                    text = 0
                else:
                    valid = True
            except:
                text = 255
            if not valid:
                channelNumber = QTableWidgetItem(str(text))
                self.table.setItem(row,column,channelNumber)
        self.updateChannelDropdowns()

    def orderChanged(self):
        pass  #order of table changed


    def updateChannelDropdowns(self):
        if self.rgbRadio.isChecked():
            self.redChannelInput.clear()
            self.greenChannelInput.clear()
            self.blueChannelInput.clear()
            for i in range(self.table.rowCount()):
                channelName = self.table.item(i,0).text()
                self.redChannelInput.addItem(channelName)
                self.greenChannelInput.addItem(channelName)
                self.blueChannelInput.addItem(channelName)
        else: #so intensity radio is checked
            self.intensityChannelInput.clear()
            for i in range(self.table.rowCount()):
                channelName = self.table.item(i,0).text()
                self.intensityChannelInput.addItem(channelName)
        if self.panTiltCheckBox.isChecked():
            self.panChannelInput.clear()
            self.tiltChannelInput.clear()
            for i in range(self.table.rowCount()):
                channelName = self.table.item(i,0).text()
                self.panChannelInput.addItem(channelName)
                self.tiltChannelInput.addItem(channelName)


    def addChannelButtonClicked(self):
        rowCount = self.table.rowCount()
        self.table.insertRow(rowCount)
        channelName = QTableWidgetItem("channel name")
        self.table.setItem(rowCount,0,channelName)
        channelNumber = QTableWidgetItem(str(255))
        self.table.setItem(rowCount,1,channelNumber)
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chkBoxItem.setTextAlignment(Qt.AlignCenter)
        chkBoxItem.setCheckState(Qt.Unchecked)
        self.table.setItem(rowCount,2,chkBoxItem)
        self.checkBoxes.append(chkBoxItem)
        self.updateChannelDropdowns()

    def deleteButtonClicked(self):
        rowsToDelete = []
        for row in range(self.table.rowCount()):
            if self.table.item(row,2).checkState():
                rowsToDelete.append(row)
        if len(rowsToDelete) > 0:
            self.confirmWindow = ConfirmWindow(self,"Are you sure you want to remove this channel?")
            if self.removeConfirmed:
                self.removeConfirmed = False
                rowsToDelete.sort(reverse=True) #needs to be in reverse otherwise will delete the wrong channels as if deletes the first then the order changes
                for row in rowsToDelete:
                    self.table.removeRow(row)
        else:
            self.errorWindow = ErrorWindow("No channels are selected. Try selecting a channel to delete one.")
        self.updateChannelDropdowns()



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



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = CreateLightTypeWindow()
    win.show()
    sys.exit(app.exec_())
