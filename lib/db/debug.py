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
		
	def connection(self, server, port, token, user):
		from modules.colors import bcolors
		
		try:
			ircsocket = socket(AF_INET, SOCK_STREAM)
			ircsocket.connect((server, port))
			print(bcolors.RED + "DEBUG: Connection success: {}, {}".format(server, port))
			try:
				cFile = open('config/channels.json')
			except:
				cFile = open('lib/db/config/channels.json')
			channels = json.load(cFile)
			print("DEBUG: loaded: channels = json.load(cFile)")
			sock_token = "PASS {}\n".format(data[2])
			sock_username = "NICK {}\n".format(data[3])
			
			#Authentification
			try:
				ircsocket.send(sock_token.encode("utf-8"))
				ircsocket.send(sock_username.encode("utf-8"))
				for i in channels['channels']:
					sock_channel = "JOIN {}\n".format(i)
					ircsocket.send(sock_channel.encode("utf-8"))
					print(bcolors.PURPLE + "Joined Channel: {}".format(i))
			except:
				print(bcolors.RED + "DEBUG: #Authentification failed")
		except:
			print(bcolors.RED + "DEBUG: Connection failed")
			
#ask [server, port, token, user]
def input_data():
	global data
	data = []
	for i in range(1, 4+1):
		if i == 1:
			server_input = input("Server Input: ")
			if server_input == "":
				data.append("irc.chat.twitch.tv")
			elif server_input != "irc.chat.twitch.tv":
				data_input = gethostbyname(server_input)
				#data_input = int(data_input)
				data.append(data_input)
			else:
				data.append("irc.chat.twitch.tv")
		elif i == 2:
			port_input = input("Port Input: ")
			if port_input == "":
				data.append(int(6667))
			elif port_input != 6667:
				data_input = int(port_input)
				data.append(data_input)
			else:
				data.append(int(6667))
		elif i == 3:
			data_input = input("OAUTH Token Input: ")
			data.append(data_input)
		elif i == 4:
			data_input = input("Username Input: ")
			data.append(data_input)
	print(data)
	print(" ")
	
if __name__ == "__main__":
	from modules.colors import bcolors
	#data[0] = server
	#data[1] = port
	#data[2] = auth token
	#data[3] = user
	
	#build connection
	#join channel -> read from channel list
	
	print("DEBUG: check_color()")
	check_color()
	print("DEBUG: banner()")
	banner()
	print(bcolors.RED + "DEBUG: input_data()")
	input_data()
	print("DEBUG: bot = irc(data[0], data[1], data[2], data[3])") 
	bot = irc(data[0], data[1], data [2], data[3])
	print("DEBUG: bot.connection(data[0], data[1])")
	bot.connection(data[0], data[1], data [2], data[3])
    
