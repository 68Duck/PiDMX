import paramiko
from scp import SCPClient
from getpass import getpass
import os
from os import path

from raspberryPiLoginWindow import RaspberryPiLoginWindow
from errorWindow import ErrorWindow

class SSHUpdateDatabase(object):
    def __init__(self,lightDisplay=None):
        self.lightDisplay = lightDisplay
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.raspberryPiLoginWindow = RaspberryPiLoginWindow(self)
        self.raspberryPiLoginWindow.show()
        self.counter = 0

    def runComputerDMX(self):
        self.lightDisplay.runComputerDMX()

    def runWithoutDMX(self):
        self.lightDisplay.runWithoutDMX()

    def login(self):
        password = self.raspberryPiLoginWindow.password
        # password = getpass() #put a paramater for message if want to change
        try:
            piIpv4 = "192.168.0.70"
            self.client.connect(piIpv4,"22","pi",password)
            if self.lightDisplay is None:
                pass
            else:
                self.lightDisplay.password = password
            print("logged in")

        except paramiko.ssh_exception.AuthenticationException:
            self.errorWindow = ErrorWindow("Incorrect password. Please try again")
            print("Incorrect password. Please try again")
            return
        except TimeoutError:
            self.errorWindow = ErrorWindow("Could not connect. Please try again later")
            print("Could not connect. Please try again later")
            return
        self.updateDatabase()
        self.lightDisplay.sshPasswordInputed()
        self.raspberryPiLoginWindow.close()

    def updateDatabase(self):
        scp = SCPClient(self.client.get_transport())
        databaseLocation = path.join(os.path.dirname(os.getcwd()),"databases")
        db = "universeValues.db"
        db = path.join(databaseLocation,db)
        scp.put(db,recursive=True,remote_path="/var/www/dmx")
        self.counter += 1
        print("updated"+str(self.counter))
        scp.close()


    def __del__(self):
        self.client.close()


if __name__ == "__main__":
    ssh = SSHUpdateDatabase()
