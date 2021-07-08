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
	
	def __init__(self, server, port, token, user):
		self.server = server
		self.port = port
		self.token = token
		self.user = user
		
	def connection(self, server, port, token, user):
		from modules.colors import bcolors
		
		try:
			global ircsocket
			ircsocket = socket.socket()
			ircsocket.connect((server, port))
			print(bcolors.RED + "DEBUG: Connection success: {}, {}".format(server, port))
			try:
				cFile = open('config/channels.json')
			except:
				cFile = open('lib/db/config/channels.json')
			channels = json.load(cFile)
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
	get = irc(data[0], data[1], data [2], data[3])
	print("DEBUG: bot.connection(data[0], data[1])")
	get.connection(data[0], data[1], data [2], data[3])
	bot = irc(data[0], data[1], data [2], data[3])
	
	while True:
		time.sleep(2)
		print(bcolors.RED + "DEBUG: buffer = bot.receive()")
		buffer = bot.receive()
		print("DEBUG: resp, buffer = buffer.split('\n', 1)")
		resp, buffer = buffer.split('\n', 1)
		print("DEBUG: if resp.startswith('PING'):")
		if resp.startswith('PING'):
				bot.send("PONG", "")
				print("Pong send")
		print("DEBUG: resplit = resp.strip().split()")
		resplit = resp.strip().split()
		if resplit[1] == "PRIVMSG":
			try:
				msg = resp.strip().split(":", 2) # split(":", 2)
				msg_split = msg[2].split(" ")
				chan = msg[1].split("PRIVMSG")[1].strip()
				user = msg[1].split("!")[0]
				print("DEBUG: try")
			except:
				log(err_log, "******\n{} ER MSG:\n{}\n\nOF MSG:\n{}\n".format(msg, resp))
				continue
			if msg_split[0] == "test":
				print(msg_split[0])
					