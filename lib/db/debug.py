import json
import os
import subprocess
import socket
import requests

from time import sleep
from pyfiglet import Figlet

subprocess.call('clear', shell=True)


def init_update():
	if os.path.basename(__file__) == 'main.py':
		pass # TODO: Auto-Update using Git


def check_color():
	try:
		from modules.colors import bcolors
	except ModuleNotFoundError:
		print("modules/colors.py seems missing. Did you install this program correctly?")
		exit()


def banner():
	from modules.colors import bcolors
	title = Figlet(font="banner3-D")
	print(bcolors.PURPLE + title.renderText("TFARMER"))


def get_config():
	# Error Handling already happened in launcher
	config_file = open('lib/db/config/config.json')

	return json.load(config_file)


def get_data(cfg):
	username = cfg['credentials']['username']
	token = cfg['credentials']['token']
	server = 'irc.chat.twitch.tv'
	port = 6667

	return [username, token, server, port]


class IRC:
	
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
	channel_name =  channel_privmsg[1:]
	contents = requests.get('https://www.twitch.tv/' + channel_name).content.decode('utf-8')
	if 'isLiveBroadcast' in contents:
		print(f"Channel: {channel_name} is live")
		return True
	else:
		print(f"Channel: {channel_name} is offline")
		return False

def is_owner(channel_privmsg, user):
	channel_name = channel_privmsg[1:]
	if channel_name == user:
		print(bcolors.GREEN + "User: {} is owner".format(user))
		return True
	else:
		print(bcolors.GREEN + "User: {} is not owner. \n {} tried to fool us !!!!".format(user))
		return False


if __name__ == "__main__":
	from modules.colors import bcolors
	init_update()
	check_color()
	banner()

	config = get_config()
	data = get_data(config)

	get = IRC(data[0], data[1], data [2], data[3])
	get.connection(data[0], data[1], data [2], data[3])
	bot = IRC(data[0], data[1], data [2], data[3])
	
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
					print(bcolors.RED + "Exception in buffer_to_irc_chat(buffer_splited):")
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
					print("Error while resplitting:\n=============")
					print("msg:\n" + msg + "\n=============")
					print("resp:\n" + resp)
					# TODO: Error-Log to file
					continue
				
				if msg_split[0] == "funnymomentspog":
					print(bcolors.GREEN + "Channel: {} => {}".format(channel_privmsg, msg_split[0]))

				elif msg_split[0] == "!raffle":
					print(bcolors.GREEN + "Channel: {} => !raffle".format(channel_privmsg))
					if isLiveBroadcast(channel_privmsg) is True:
						if is_owner(channel_privmsg, user) is True:
							sleep(10)
							print(bcolors.BLUE + "BOT: Send '!join' to Channel: {}".format(channel_privmsg)) 
							bot.answer(channel_privmsg, '!join')
						elif is_owner(channel_privmsg, user) is False:
							print(bcolors.RED + "---")
					elif isLiveBroadcast(channel_privmsg) is False:
						print(bcolors.GREEN + "BOT: {} tried to fool us :P".format(channel_privmsg))
