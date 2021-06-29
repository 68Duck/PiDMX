from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PIL import Image
import math as maths
from os import path,mkdir
import easygui

from errorWindow import ErrorWindow


class CreateSpriteWindow(QWidget,uic.loadUiType(path.join("ui","createSpriteWindow.ui"))[0]):
    def __init__(self,imageName,parentWindow):
        super().__init__()
        self.setupUi(self)
        self.setMouseTracking(True)
        if not path.exists("images"):
            mkdir("images")
            self.errorWindow = ErrorWindow("The images folder does not exists. Creating a new images folder.")

        self.imageName = imageName
        self.parentWindow = parentWindow
        if self.imageName[len(self.imageName)-3:len(self.imageName)] != ".png":
            self.imageName = self.imageName + ".png"
        self.parentWindow.imageName = self.imageName
        self.setWindowTitle("Image Edit Window")
        self.creatingBox = False
        self.creatingCircle = False
        self.creatingChangingBox = False
        self.creatingChangingCircle = False
        self.labels = []
        try:
            self.image = Image.open(path.join("images",self.imageName))
        except FileNotFoundError:
            self.image = Image.new("RGB",(500,500),color="black")
            self.image.save(path.join("images",self.imageName))

        self.pixels = self.image.load()
        self.setGeometry(250,250,750,750)
        self.imageLabel = QLabel(self)
        self.saveImage()
        self.imageLabel.move(25,25)

        self.createBoxButton.clicked.connect(self.createBoxButtonPressed)
        self.createCircleButton.clicked.connect(self.createCircleButtonPressed)
        self.createBoxSlider.valueChanged.connect(self.boxSliderChangedValue)
        self.createCircleSlider.valueChanged.connect(self.circleSliderChangedValue)
        self.newImageButton.clicked.connect(self.newImageButtonPressed)
        self.penSizeSlider.valueChanged.connect(self.penSizeSliderChangedValue)
        self.eraserSizeSlider.valueChanged.connect(self.eraserSizeSliderChangedValue)
        self.penButton.clicked.connect(self.penButtonClicked)
        self.eraserButton.clicked.connect(self.eraserButtonClicked)
        self.colourChangingRadio.clicked.connect(self.radioChanged)
        self.backgroundRadio.clicked.connect(self.radioChanged)
        self.openImageButton.clicked.connect(self.openImageButtonClicked)
        self.penSizeSliderChangedValue()
        self.eraserSizeSliderChangedValue()
        self.boxSliderChangedValue()
        self.circleSliderChangedValue()

        self.previousPosition = None

    def openImageButtonClicked(self):
        # print(easygui.fileopenbox())
        openedImage = easygui.fileopenbox()
        try:
            self.image = Image.open(openedImage)
            self.image = self.image.resize((500,500))
            self.pixels = self.image.load()
        except:
            self.errorWindow = ErrorWindow("That file cannot be read as an image. Please try again.")
            self.openImageButtonClicked()
        # self.image = Image.open(easygui.fileopenbox())
        self.saveImage()

    def newImageButtonPressed(self):
        for i in range(self.image.width):
            for j in range(self.image.height):
                self.pixels[i,j] = (0,0,0)
        # self.image = Image.new("RGB",(500,500),color="black")
        self.saveImage()

    def penSizeSliderChangedValue(self):
        self.penSizeLabel.setText(f"Pen Size: {self.penSizeSlider.value()}")

    def eraserSizeSliderChangedValue(self):
        self.eraserSizeLabel.setText(f"Eraser Size: {self.eraserSizeSlider.value()}")

    def circleSliderChangedValue(self):
        self.circleSizeLabel.setText(f"Circle Size: {self.createCircleSlider.value()}")

    def boxSliderChangedValue(self):
        self.boxSizeLabel.setText(f"Box Size: {self.createBoxSlider.value()}")

    def createBoxButtonPressed(self):
        self.creatingCircle = False
        self.createCircleButton.setChecked(False)
        self.penButton.setChecked(False)
        if self.sender().isChecked():
            self.creatingBox = True
        else:
            self.creatingBox = False

    def radioChanged(self):
        if self.backgroundRadio.isChecked():
            if self.creatingChangingCircle:
                self.creatingCircle = True
                self.creatingChangingCircle = False
            if self.creatingChangingBox:
                self.creatingBox = True
                self.creatingChangingBox = False
        else: #so colour changing radio is checked
            if self.creatingCircle:
                self.creatingCircle = False
                self.creatingChangingCircle = True
            if self.creatingBox:
                self.creatingBox = False
                self.creatingChangingBox = True


    def penButtonClicked(self):
        if self.penButton.isChecked():
            self.creatingBox = False
            self.creatingCircle = False
            self.creatingChangingBox = False
            self.creatingChangingCircle = False
            self.createBoxButton.setChecked(False)
            self.createCircleButton.setChecked(False)
            self.eraserButton.setChecked(False)

    def eraserButtonClicked(self):
        if self.sender().isChecked():
            self.creatingBox = False
            self.creatingCircle = False
            self.creatingChangingBox = False
            self.creatingChangingCircle = False
            self.createBoxButton.setChecked(False)
            self.createCircleButton.setChecked(False)
            self.penButton.setChecked(False)

    def createCircleButtonPressed(self):
        self.creatingBox = False
        self.createBoxButton.setChecked(False)
        self.penButton.setChecked(False)
        self.eraserButton.setChecked(False)
        if self.sender().isChecked():
            if self.colourChangingRadio.isChecked():
                self.creatingChangingCircle = True
                self.creatingCircle = False
            else:
                self.creatingChangingCircle = False
                self.creatingCircle = True

        else:
            self.creatingChangingCircle = False
            self.creatingCircle = False

    def setPixel(self,x,y,colour):
        if x > 0 and x < self.image.width:
            if y > 0 and y < self.image.height:
                self.pixels[x,y] = colour

    # def createLine(self,firstPoint,secondPoint,width): #does something weird but creates an interresting font
    #     x0,y0 = firstPoint
    #     x1,y1 = secondPoint
    #     ax = 1 if (x0<x1) else -1
    #     ay = 1 if (y0<y1) else -1
    #
    #     for i in range(width):
    #         fp = (firstPoint[0]+ax*i,firstPoint[1]+ay*i)
    #         sp = (secondPoint[0]+ax*i,secondPoint[1]+ay*i)
    #
    #         x0,y0 = fp
    #         x1,y1 = sp
    #         dy = abs(y1-y0)
    #         dx = abs(x1-x0)
    #         sx = 1 if (x0<x1) else -1
    #         sy = 1 if (y0<y1) else -1
    #         err = dx-dy
    #
    #         while True:
    #             self.setPixel(x0,y0,(255,255,255))
    #             if x0 == x1 and y0 == y1:
    #                 break
    #             else:
    #                 e2 = 2*err
    #                 if e2 > -dy:
    #                     err -= dy
    #                     x0 += sx
    #                 if e2 < dx:
    #                     err += dx
    #                     y0 += sy
    def createLine(self,firstPoint,secondPoint,width):
        x0,y0 = firstPoint
        x1,y1 = secondPoint
        dy = abs(y1-y0)
        dx = abs(x1-x0)
        sx = 1 if (x0<x1) else -1
        sy = 1 if (y0<y1) else -1
        err = dx-dy

        while True:
            xpos = x0
            ypos = y0
            for i in range(width):
                for j in range(width):
                    if maths.sqrt(i**2+j**2)>width:
                        pass
                    else:
                        self.setPixel(xpos+i,ypos+j,(255,255,255))
                        self.setPixel(xpos+i,ypos-j,(255,255,255))
                        self.setPixel(xpos-i,ypos+j,(255,255,255))
                        self.setPixel(xpos-i,ypos-j,(255,255,255))
            # self.setPixel(x0,y0,(255,255,255))
            if x0 == x1 and y0 == y1:
                break
            else:
                e2 = 2*err
                if e2 > -dy:
                    err -= dy
                    x0 += sx
                if e2 < dx:
                    err += dx
                    y0 += sy




    def mouseReleaseEvent(self,e):
        print("test")
        self.previousPosition = None

    def mousePressEvent(self,e):
        if self.creatingBox:
            xpos = e.x()-self.imageLabel.x()
            ypos = e.y()-self.imageLabel.y()
            self.boxSize = self.createBoxSlider.value()
            for i in range(self.boxSize):
                for j in range(self.boxSize):
                    self.setPixel(xpos+i,ypos+j,(255,255,255))
        elif self.creatingCircle:
            xpos = e.x()-self.imageLabel.x()
            ypos = e.y()-self.imageLabel.y()
            self.circleSize = self.createCircleSlider.value()
            for i in range(self.circleSize):
                for j in range(self.circleSize):
                    if maths.sqrt(i**2+j**2)>self.circleSize:
                        pass
                    else:
                        self.setPixel(xpos+i,ypos+j,(255,255,255))
                        self.setPixel(xpos+i,ypos-j,(255,255,255))
                        self.setPixel(xpos-i,ypos+j,(255,255,255))
                        self.setPixel(xpos-i,ypos-j,(255,255,255))

        elif self.creatingChangingCircle:
            xpos = e.x()-self.imageLabel.x()
            ypos = e.y()-self.imageLabel.y()
            if xpos > 0 and xpos < self.image.width:
                if ypos > 0 and ypos < self.image.width:
                    self.circleLabel = QLabel(self)
                    self.labels.append(self.circleLabel)
                    self.circleSize = self.createCircleSlider.value()
                    radius = self.circleSize #I don't think it is actually the radius. Probably is diameter
                    self.circleLabel.move(e.x()-int(radius/2),e.y()-int(radius/2))
                    self.circleLabel.setFixedSize(radius,radius)
                    borderWidth = int(radius/2)
                    self.circleLabel.type = "circle"
                    self.circleLabel.setStyleSheet(f"background-color:#ffff00;border-radius:{borderWidth};border: 3px solid #ffff00")
                    self.circleLabel.show()

        elif self.creatingChangingBox:
            xpos = e.x()-self.imageLabel.x()
            ypos = e.y()-self.imageLabel.y()
            if xpos > 0 and xpos < self.image.width:
                if ypos > 0 and ypos < self.image.width:
                    self.boxLabel = QLabel(self)
                    self.labels.append(self.boxLabel)
                    self.boxSize = self.createBoxSlider.value()
                    self.boxLabel.move(e.x()-int(self.boxSize/2),e.y()-int(self.boxSize/2))
                    self.boxLabel.setFixedSize(self.boxSize,self.boxSize)
                    self.boxLabel.type = "square"
                    self.boxLabel.setStyleSheet(f"background-color:#ffff00;border: 3px solid #ffff00")
                    self.boxLabel.show()
        else:
            xpos = e.x()-self.imageLabel.x()
            ypos = e.y()-self.imageLabel.y()
            if self.previousPosition is not None:
                self.createLine((xpos,ypos),self.previousPosition,self.penSizeSlider.value())
            if xpos > 0 and xpos < self.image.width:
                if ypos > 0 and ypos < self.image.width:
                    self.previousPosition = (xpos,ypos)
            # if self.penButton.isChecked():
            #     colour = (255,255,255)
            #     self.circleSize = self.penSizeSlider.value()
            # else: # elif self.eraserButton.isChecked():
            #     colour = (0,0,0)
            #     self.circleSize = self.eraserSizeSlider.value()
            #     for label in self.labels:
            #         x = label.x()
            #         y = label.y()
            #         if e.x() > x and e.x() < x+label.width():
            #             if e.y() > y and e.y() < y+label.height():
            #                 label.hide()
            #                 self.labels.remove(label)
            # for i in range(self.circleSize):
            #     for j in range(self.circleSize):
            #         if maths.sqrt(i**2+j**2)>self.circleSize:
            #             pass
            #         else:
            #             self.setPixel(xpos+i,ypos+j,colour)
            #             self.setPixel(xpos+i,ypos-j,colour)
            #             self.setPixel(xpos-i,ypos+j,colour)
            #             self.setPixel(xpos-i,ypos-j,colour)
        self.saveImage()

    def mouseMoveEvent(self,e):
        if self.creatingBox:
            pass
        elif self.creatingCircle:
            pass
        else:
            self.mousePressEvent(e)

    def saveImage(self):
        try: #stops permission denied error
            self.image.save(path.join("images",self.imageName))
        except:
            pass
        pixmap = QPixmap(path.join("images",self.imageName))
        self.imageLabel.setPixmap(pixmap)

    def closeEvent(self,event):
        self.saveImage()
        self.parentWindow.indicators = self.labels

class Test:
    def __init__(self):
        self.image = None

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = CreateSpriteWindow("sadfhsadfhkljsadfhkljasdhsdfjk",Test())
    win.show()
    sys.exit(app.exec_())
