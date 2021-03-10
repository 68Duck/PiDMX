from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class PanTiltGridWindow(QWidget,uic.loadUiType("panTiltGrid.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Pan and Tilt")
        self.crossH.setGeometry(100-10,100-2,20,4)
        self.crossV.setGeometry(100-2,100-10,4,20)
        self.initUI()

    def initUI(self):
        pass

    def mouseMoveEvent(self,e):
        x=e.x()
        y=e.y()
        self.coordsClicked(x,y)

    def mousePressEvent(self,e):
        x=e.x()
        y=e.y()
        self.coordsClicked(x,y)

    def coordsClicked(self,x,y):
        if x > 550:
            x = 550
        if x < 50:
            x = 50
        if y > 550:
            y = 550
        if y < 50:
            y = 50
        mouseDifference = 50
        self.crossH.setGeometry(x-10-mouseDifference,y-2-mouseDifference,20,4)
        self.crossV.setGeometry(x-2-mouseDifference,y-10-mouseDifference,4,20)

    def paintEvent(self,e=None):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.red, 1, Qt.SolidLine)

        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(50, 300, 550, 300)
        qp.drawLine(300, 50, 300, 550)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = PanTiltGridWindow()
    win.show()
    sys.exit(app.exec_())
