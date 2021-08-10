from PyQt5 import QtCore,uic
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel
# from PyQt5.QtGui import Qt
from PyQt5.QtCore import QEvent,Qt

class Bar(object):
    def __init__(self,barName,x,y,width,height,isHorizontal,barsEditWindow):
        self.pos = (x,y)
        self.width = width
        self.height = height
        self.name = barName
        self.isHorizontal = isHorizontal
        self.barsEditWindow = barsEditWindow
        self.selected = False
        self.points = []
        self.createShapes()
        # self.setSelected(True)  #remove me

    def createShapes(self):
        self.bar = QLabel(self.barsEditWindow)
        x,y = self.pos
        self.bar.move(x,y)
        self.bar.setStyleSheet("background-color:white; border: 1px solid white;")
        self.bar.setFixedSize(self.width,self.height)
        if self.isHorizontal:
            self.label = self.createBarLabel(x+self.width+50,y+self.height//2-25)
        else:
            self.label = self.createBarLabel(x-25+self.width//2,y-75)

    def createBarLabel(self,x,y):
        label = QLabel(self.barsEditWindow)
        label.move(int(x),int(y))
        label.setFixedSize(50,50)
        label.setStyleSheet("background-color:white; border: 1px solid white;font-size: 30px;")
        label.setText(self.name)
        label.setAlignment(Qt.AlignCenter)
        return label

    def show(self):
        self.bar.show()
        self.label.show()

    def hide(self):
        self.bar.hide()
        self.label.hide()
        for point in self.points:
            point.hide()

    def checkIfInRange(self,xPos,yPos):
        x,y = self.pos
        if xPos>x and xPos<x+self.width:
            if yPos>y and yPos<y+self.height:
                return True #as in the bar clickable range
        return False

    def setSelected(self,selected):
        self.selected = selected
        if selected:
            x,y = self.pos
            width = self.width
            height = self.height
            self.p0 = Point(x,y,self,[1,0,0,1])
            self.p1 = Point(x+width/2,y,self,[0,0,0,1])
            self.p2 = Point(x+width,y,self,[1,1,0,0])
            self.p3 = Point(x,y+height/2,self,[1,0,0,0])
            self.p4 = Point(x+width,y+height/2,self,[0,1,0,0])
            self.p5 = Point(x,y+height,self,[0,0,1,1])
            self.p6 = Point(x+width/2,y+height,self,[0,0,1,0])
            self.p7 = Point(x+width,y+height,self,[0,1,1,0])
            self.points = []
            for i in range(8):
                self.points.append(getattr(self,f"p{i}"))

        else:
            for point in self.points:
                point.hide()

    def swapPointsTopAndBottom(self):
        for point in self.points:
            if point.position[0]:
                point.position[0] = 0
                point.position[2] = 1
            elif point.position[2]:
                point.position[0] = 1
                point.position[2] = 0

    def swapPointsLeftAndRight(self):
        for point in self.points:
            if point.position[1]:
                point.position[1] = 0
                point.position[3] = 1
            elif point.position[3]:
                point.position[1] = 1
                point.position[3] = 0

    def pointsMoved(self,position,point):
        self.bar.hide()
        self.label.hide()
        top = position[0]
        right = position[1]
        bottom = position[2]
        left = position[3]
        x,y = self.pos
        if top:
            dy = y-point.y
            y = point.y
            self.height += dy
            if self.height < 0:
                self.height = abs(self.height)
                y = y-self.height
                point.swapTB()
        if left:
            dx = x-point.x
            x = point.x
            self.width += dx
            if self.width < 0:
                self.width = abs(self.width)
                x = x - self.width
                point.swapLR()
        if bottom:
            self.height = point.y - y
            if self.height < 0:
                self.height = abs(self.height)
                y=point.y
                point.swapTB()
        if right:
            self.width = point.x - x
            if self.width < 0:
                self.width = abs(self.width)
                x = point.x
                point.swapLR()
        self.pos = (x,y)
        self.setSelected(False) #so hides all current points
        self.setSelected(True) #so creats new points
        self.createShapes()
        self.bar.show()
        self.label.show()
        self.barsEditWindow.updateBarsInDatabase()

    def setPosition(self,pos):
        self.pos = pos
        self.label.hide()
        self.bar.hide()
        self.createShapes()
        self.setSelected(False) #so hides all current points
        self.setSelected(True) #so creats new points
        self.bar.show()
        self.label.show()
        self.barsEditWindow.updateBarsInDatabase()


class Point(object):
    def __init__(self,x,y,bar,position):
        self.position = position  #positions is an array length 4 representing [top,right,bottom,left]
        self.x = x
        self.y = y
        self.bar = bar
        self.width,self.height = [10,10]
        self.createShape()

    def createShape(self):
        self.label = QLabel(self.bar.barsEditWindow)
        self.label.move(self.x-self.width//2,self.y-self.height//2)
        self.label.setFixedSize(self.width,self.height)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color:white;border: 2px solid lightgrey; border-radius:100%;")
        self.label.show()

    def hide(self):
        self.label.hide()

    def show(self):
        self.label.show()

    def checkIfInRange(self,xPos,yPos):
        # print(xPos,yPos,self.x,self.y)
        if xPos>self.x-self.width//2 and xPos<self.x+self.width:
            if yPos>self.y-self.height//2 and yPos<self.y+self.height:
                return True #as in the bar clickable range
        return False

    def setPosition(self,x=False,y=False):
        if x is not False:
            self.x = x
        if y is not False:
            self.y = y
        self.label.hide()
        # self.createShape()
        self.bar.pointsMoved(self.position,self)

    def swapLR(self):
        if self.position[1]:
            self.position[1] = 0
            self.position[3] = 1
        elif self.position[3]:
            self.position[1] = 1
            self.position[3] = 0

    def swapTB(self):
        if self.position[0]:
            self.position[0] = 0
            self.position[2] = 1
        elif self.position[2]:
            self.position[0] = 1
            self.position[2] = 0
