from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import sys
import os

from lightDisplay import LightDisplay
from logonWindow import LogonWindow

# PyQt exception handling isn't good
# so we have to add our own
# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

# needed to catch exceptions from the UI
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    # Could quit the program at this point
    # sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    devMode = False
    lightDisplay = LightDisplay([],app=app,devMode=devMode)
    # win = LogonWindow(lightDisplay)
    # win.show()
    sys.exit(app.exec_())


#curl -L "https://api.codetabs.com/v1/loc?github=68Duck/PiDMX"
#Run this to ge the number of lines in the program
