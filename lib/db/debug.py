import json
import time
import os
import subprocess
import socket
import pyfiglet
import sys
import threading
import requests

from time import sleep
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
	def answer_irc(self, channel, message):
		c = "PRIVMSG {} :{}\r\n".format(channel, message).encode("utf-8")
			
	def answer(self, channel_privmsg, message):
		irc_message = "PRIVMSG {} :{}\r\n".format(channel_privmsg, message).encode("utf-8")
		ircsocket.send(irc_message)
#ask [server, port, token, user]

def isLiveBroadcast(channel_privmsg):
	contents = request.get('https://www.twitch.tv/' + channel_privmsg).content.decode('utf-8')
	if 'isLiveBroadcast' in contents:
		print(f"Channel: {channel_privmsg} is live")
		return True
	else:
		print(f"Channel: {channel_privmsg} is offline")
		return False

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
	print(bcolors.LIGHT_WHITE + ":::..:::::..::::::::..:::::..::..:::::..::..:::::..::........::..:::::..::")
	print(bcolors.PURPLE + " ")
	
	while True:
		buffer = bot.receive()
		if buffer is not None:
			
			show_chat = False
			
			#Filter Chat into string and append space character
			if show_chat is True:
				try:
					buffer_splited = buffer.split()
					def buffer_to_irc_chat(buffer_splited):
						irc_string = ""
						for i in range(0, 2):
							buffer_splited.pop(i)
						for element in buffer_splited:
							irc_string += element + " "
						return irc_string
					print(bcolors.LIGHT_WHITE + buffer_to_irc_chat(buffer_splited))
				except:
					pritn(bcolors.RED + "Exception in buffer_to_irc_chat(buffer_splited):")
					pass
			
			resp, buffer = buffer.split('\n', 1)
			if resp.startswith('PING'):
				bot.send("PONG", "")
				print(bcolors.PURPLE + "Pong send")
			resplit = resp.strip().split()

			if resplit[1] == "PRIVMSG":
				try:
					msg = resp.strip().split(":", 2) # split(":", 2)
					msg_split = msg[2].split(" ")
					channel_privmsg = msg[1].split("PRIVMSG")[1].strip()
					user = msg[1].split("!")[0]
				except:
					log(f"******\nMSG:\n{msg}\n\nOF MSG:\n{resp}\n")
					continue
				
				if msg_split[0] == "funnymomentspog":
					print(bcolors.GREEN + "Channel: {} => {}".format(channel_privmsg, msg_split[0]))

				elif msg_split[0] == "!raffle":
					try:
						if isLiveBroadcast(channel_privmsg) is True:
							print(bcolors.GREEN + "Channel: {}  => !raffle init.".format(channel_privmsg)) 
							sleep(10) 
							bot.answer(channel_privmsg, '!joins')
					except:
						print(bcolors.RED + "Exception in isLiveBroadcast!")
