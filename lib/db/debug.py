import json
import time
import os
import subprocess
import socket
import pyfiglet
import sys
import asyncio

from pyfiglet import Figlet
from socket import *
from socket import gethostbyname

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
		self.user = user
		
	def connection(self, server, port):
		from modules.colors import bcolors
		
		try:
			print(bcolors.BLUE + "DEBUG: Connection failed")
			ircsocket = socket(AF_INET, SOCK_STREAM)
			ircsocket.connect((server, port))
			print("DEBUG: Connection success")
		except:
			print(bcolors.BLUE + "DEBUG: Connection failed")
			
#ask [server, por, token, user]
def input_data():
	global data
	data = []
	for i in range(1, 4+1):
		if i == 1:
			server_input = input("Server Input: ")
			data_input = gethostbyname(server_input)
			#data_input = int(data_input)
			data.append(data_input)
		elif i == 2:
			port_input = input("Port Input: ")
			data_input = int(port_input)
			data.append(data_input)
		elif i == 3:
			data_input = input("OAUTH Token Input: ")
			data.append(data_input)
		elif i == 4:
			data_input = input("Username Input: ")
			data.append(data_input)
	print(data)
	print(" ")

	
if __name__ == "__main__":
    check_color()
    banner()
    input_data()
    bot = irc(data[0], data[1], data [2], data[3])
    bot.connection(data[0], data[1])
    
