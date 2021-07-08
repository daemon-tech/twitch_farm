import json
import time
import os
import subprocess
import socket
import pyfiglet
import sys

from pyfiglet import Figlet
from socket import *

subprocess.call('clear', shell=True)

'''#Check dependencies
def init_update():
    try:
        os.system("git pull")
    except:
        pass'''

def check_color():
	try:
		from modules.colors import bcolors
	except:
		print(f"DEBUG: lib/db/modules/colors.py missing")
		exit()

def banner():
	from modules.colors import bcolors
	title = Figlet(font="banner3-D")
	print(bcolors.PURPLE + title.renderText("TFARMER"))

class irc:
	def __init__(self, server, port, token, user):
		self.server = server
		self.port = port
		self.token = token
		self.user = username
		
	def connection(server, port):
		self.ircsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ircsocket.connect((self.server, self.port))
		
#ask [server, por, token, user]
def input_data():
	data = []
	for i in range(1, 4+1):
		if i == 1:
			data_input = input("Server Input: ")
			data.append(data_input)
		elif i == 2:
			data_input = input("Port Input: ")
			data.append(data_input)
		elif i == 3:
			data_input = input("OAUTH Token Input: ")
			data.append(data_input)
		elif i == 4:
			data_input = input("Username Input")
			data.append(data_input)
	print(data)

	
if __name__ == "__main__":
    check_color()
    banner()
    input_data()
    bot = irc(data[0], data[1], data [2], data[3])
    
