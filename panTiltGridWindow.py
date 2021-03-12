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
        self.panSlider.valueChanged[int].connect(self.panSliderChangedValue)
        self.tiltSlider.valueChanged[int].connect(self.tiltSliderChangedValue)
        self.panTextInput.textEdited.connect(self.panTextChangedValue)
        self.tiltTextInput.textEdited.connect(self.tiltTextChangedValue)

    def panSliderChangedValue(self):
        self.panTextInput.setText(str(self.panSlider.value()))

    def tiltSliderChangedValue(self):
        self.tiltTextInput.setText(str(self.tiltSlider.value()))

    def panTextChangedValue(self):
        try:
            self.panText = int(self.panTextInput.text())
            if int(self.panTextInput.text()) > 100:
                self.panTextInput.setText(str(100))
            if int(self.panTextInput.text()) < 1:
                self.panTextInput.setText(str(1))
            self.panSlider.setValue(int(self.panTextInput.text()))
        except:
            self.panTextInput.setText("1")
            self.panSlider.setValue(1)

    def tiltTextChangedValue(self):
        try:
            self.tiltText = int(self.tiltTextInput.text())
            if int(self.tiltTextInput.text()) > 100:
                self.tiltTextInput.setText(str(100))
            if int(self.tiltTextInput.text()) < 1:
                self.tiltTextInput.setText(str(1))
            self.tiltSlider.setValue(int(self.tiltTextInput.text()))
        except:
            self.tiltTextInput.setText("1")
            self.tiltSlider.setValue(1)

    def mouseMoveEvent(self,e):
        x=e.x()
        y=e.y()
        self.coordsClicked(x,y)

    def mousePressEvent(self,e):
        x=e.x()
        y=e.y()
        self.coordsClicked(x,y)

    def coordsClicked(self,x,y): #remove returns if want to be able to click outside
        if x > 550:
            return
            x = 550
        if x < 50:
            return
            x = 50
        if y > 550:
            return
            y = 550
        if y < 50:
            return
            y = 50
        mouseDifference = 50
        self.crossH.setGeometry(x-10-mouseDifference,y-2-mouseDifference,20,4)
        self.crossV.setGeometry(x-2-mouseDifference,y-10-mouseDifference,4,20)
        self.panSlider.setValue(int((x-mouseDifference)/5))
        self.tiltSlider.setValue(int((y-mouseDifference)/5))
        self.panSliderChangedValue()
        self.tiltSliderChangedValue()

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
