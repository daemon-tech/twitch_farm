import json
import time
import os
import subprocess
import socket
import pyfiglet
import sys
import asyncio
import logging

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
			global ircsocket
			ircsocket = socket(AF_INET, SOCK_STREAM)
			ircsocket.connect((server, port))
			print(bcolors.RED + "DEBUG: Connection success: {}, {}".format(server, port))
			cFile = open('lib/db/config/config.json')
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
					print("Connected: TOKEN: {} USER: {} CHANNEL: {}".format(sock_token, sock_username, sock_channel))
			except:
				print(bcolors.RED + "DEBUG: #Authentification failed")
		except:
			print(bcolors.RED + "DEBUG: Connection failed")
			
	def receive(self):
		return ircsocket.recv(4096).decode("utf-8")
	
	def send(self, command, message):
		c = "{} {}\r\n".format(command, message).encode("utf-8")
		ircsocket.send(c)
			
#ask [server, port, token, user]
def input_data():
	cfile = open('lib/db/config/config.json')
	credentials = json.load(cfile)

	global data
	data = []
	data.append("irc.chat.twitch.tv")
	data.append(int(6667))
	data.append(credentials['credentials']['username'])
	data.append(credentials['credentials']['token'])
	
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
	get = irc(data[0], data[1], data [2], data[3])
	print("DEBUG: bot.connection(data[0], data[1])")
	get.connection(data[0], data[1], data [2], data[3])
	
	while True:
		bot = irc(data[0], data[1], data [2], data[3])
		buffer = bot.receive()
		resp, buffer = buffer.split('\n', 1)
		if resp.startswith('PING'):
				bot.send("PONG", "")