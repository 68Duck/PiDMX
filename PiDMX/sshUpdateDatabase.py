import paramiko
from scp import SCPClient
from getpass import getpass
import os
from os import path

from DMXSelectionWindow import DMXSelectionWindow
from errorWindow import ErrorWindow
from ipv4Input import IPv4Input

class SSHUpdateDatabase(object):
    def __init__(self,lightDisplay=None):
        self.lightDisplay = lightDisplay
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.DMXSelectionWindow = DMXSelectionWindow(self)
        self.DMXSelectionWindow.show()
        self.counter = 0

    def runComputerDMX(self,port):
        self.lightDisplay.runComputerDMX(port)

    def runWithoutDMX(self):
        self.lightDisplay.runWithoutDMX()

    def login(self,raspberryPiPassword):
        # password = getpass() #put a paramater for message if want to change
        self.ipv4Input = IPv4Input(self)
        self.raspberryPiPassword = raspberryPiPassword


    def connectToPi(self,piIpv4):
        password = self.raspberryPiPassword
        try:
            # piIpv4 = "192.168.0.70"
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
        except paramiko.ssh_exception.NoValidConnectionsError: #this happend when the address is of something else so you cannot ssh into it
            self.errorWindow = ErrorWindow("The ipv4 is incorrect. Please try again.")
            print("The ipv4 is incorrect. Please try again.")
            return

        self.updateDatabase()
        self.lightDisplay.sshPasswordInputed(piIpv4)
        self.raspberryPiLoginWindow.close()

    def updateDatabase(self):
        scp = SCPClient(self.client.get_transport())
        # databaseLocation = path.join(os.path.dirname(os.getcwd()),"databases")
        db = "universeValues.db"
        db = path.join("databases",db)
        scp.put(db,recursive=True,remote_path="/var/www/dmx")
        self.counter += 1
        # print("updated"+str(self.counter))
        scp.close()


    def __del__(self):
        self.client.close()


if __name__ == "__main__":
    ssh = SSHUpdateDatabase()
