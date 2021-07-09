import json
import time
import os
import subprocess
import socket
import pyfiglet
import sys
import threading

from pyfiglet import Figlet
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
	
	def __init__(self, username, token, server, port):
		self.server = server
		self.port = port
		self.token = token
		self.user = username
		
	def connection(self, username, token, server, port):
		from modules.colors import bcolors
		
		try:
			global ircsocket
			ircsocket = socket.socket()
			ircsocket.connect((server, port))
			#print(bcolors.RED + "DEBUG: Connection success: {}, {}".format(server, port))
			cFile = open('lib/db/config/config.json')
			channels = json.load(cFile)
			sock_token = "PASS {}\n".format(data[1])
			sock_username = "NICK {}\n".format(data[0])
			
			#Authentification
			try:
				ircsocket.send(sock_token.encode("utf-8"))
				ircsocket.send(sock_username.encode("utf-8"))
				for i in channels['channels']:
					sock_channel = "JOIN {}\n".format(i)
					ircsocket.send(sock_channel.encode("utf-8"))
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
	data.append(credentials['credentials']['username'])
	data.append(credentials['credentials']['token'])
	data.append("irc.chat.twitch.tv")
	data.append(int(6667))
	
if __name__ == "__main__":
	from modules.colors import bcolors
	#data[0] = user
	#data[1] = token
	#data[2] = server
	#data[3] = port
	
	check_color()
	banner()
	input_data()
	get = irc(data[0], data[1], data [2], data[3])
	get.connection(data[0], data[1], data [2], data[3])
	bot = irc(data[0], data[1], data [2], data[3])
	
	print(" ")
	print(" ")
	print(bcolors.LIGHT_PURPLE + ":::..:::::..::::::::..:::::..::..:::::..::..:::::..::........::..:::::..::")
	print(bcolors.Purple + " ")
	
	while True:
		buffer = bot.receive()
		if buffer is not None:
			#print(bcolors.PURPLE + "IRC-CHAT: {}".format(buffer))
			resp, buffer = buffer.split('\n', 1)
			if resp.startswith('PING'):
				bot.send("PONG", "")
				print(bcolors.PURPLE + "Pong send")
			resplit = resp.strip().split()
			
			if resplit[1] == "PRIVMSG":
				
				try:
					msg = resp.strip().split(":", 2) # split(":", 2)
					msg_split = msg[2].split(" ")
					chan = msg[1].split("PRIVMSG")[1].strip()
					user = msg[1].split("!")[0]
				except:
					log(err_log, "******\n{} ER MSG:\n{}\n\nOF MSG:\n{}\n".format(msg, resp))
					continue
					
				if msg_split[0] == "debuglog":
					print(msg_split[0])
					
					
					
					
					