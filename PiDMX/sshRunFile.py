import paramiko
import time
from getpass import getpass
import keyboard
import threading
import sys

class SecureShell(object):
    def __init__(self,password):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.loggedIn = False
        piIpv4 = "192.168.0.70"
        while True:
            if password is None:
                password = getpass() #put a paramater for message if want to change
            try:
                self.client.connect(piIpv4, username='pi', password=password)
                dir = "/var/www/dmx"
                command = "sudo python piDMX.py"
                self.client.exec_command(f'cd {dir}; {command}',get_pty=True)
                self.loggedIn = True
                print("logged in")
                break
            except paramiko.ssh_exception.AuthenticationException:
                print("Incorrect password. Please try again")

    def __del__(self):
        self.client.exec_command(chr(3))



class SSHRunFile(object):
    def __init__(self,testMode = False,password = None):
        self.ssh = SecureShell(password)
        if testMode:
            while True:
                if keyboard.is_pressed("q") and self.ssh.loggedIn:
                    self.ssh.client.exec_command(chr(3))
                    print("Program stopped")
                    sys.exit()

if __name__ == "__main__":
    sshRunFile = SSHRunFile(True)
