import json
import os
import requests
import subprocess
import socket

from modules.colors import bcolors
from pyfiglet import Figlet
from time import sleep

subprocess.call('clear', shell=True)


def init_update():
	if os.path.basename(__file__) == 'main.py':
		pass # TODO: Auto-Update using Git


def print_banner():
	title = Figlet(font="banner3-D")
	print(bcolors.PURPLE + title.renderText("TFARMER"))

def print_spacer():
	print(" ")
	print(" ")
	print(bcolors.LIGHT_WHITE + ":::..:::::..::::::::..:::::..::..:::::..::..:::::..::........::..:::::..::")
	print(bcolors.PURPLE + " ")

def print_info(info_string):
	print(bcolors.PURPLE + info_string)

def print_error(err_string):
	print(bcolors.RED + err_string)


# =====================================================================================================================


def get_config():
	# Error Handling already happened in launcher
	config_file = open('lib/db/config/config.json')

	return json.load(config_file)


def get_data():
	username=''
	token=''

	try:
		username = config['credentials']['username']
		token = config['credentials']['token']
	except KeyError:
		print_error("Error: Credentials not exist or are entered incorrectly. Program will now exit.")
		exit()

	server = 'irc.chat.twitch.tv'
	port = 6667

	return [username, token, server, port]


def get_show_chat():
	try:
		return config['show_chat']
	except KeyError:
		print_error("Error: Can't find 'show_chat' configuration. Is your config.json corrupted?"
							"Program will now exit.")
		exit()


# =====================================================================================================================


def connect():

	irc_socket = socket.socket()
	irc_socket.connect((data[2], data[3]))
	sock_token = "PASS {}\n".format(data[1])
	sock_username = "NICK {}\n".format(data[0])

	# Authentication
	irc_socket.send(sock_token.encode("utf-8"))
	irc_socket.send(sock_username.encode("utf-8"))
	for i in config['channels']:
		sock_channel = "JOIN #{}\n".format(i.lower())
		irc_socket.send(sock_channel.encode("utf-8"))

	return irc_socket


def receive(irc_socket):
	return irc_socket.recv(4096).decode("utf-8")


def send(irc_socket, command, message):
	c = "{} {}\r\n".format(command, message).encode("utf-8")
	irc_socket.send(c)


def answer(irc_socket, channel_privmsg, message):
	irc_message = "PRIVMSG {} :{}\r\n".format(channel_privmsg, message).encode("utf-8")
	irc_socket.send(irc_message)


# =====================================================================================================================

def loop():
	while True:
		try:
			buffer = receive(socket)
		except ConnectionResetError:
			print_error("Connection was reset by Twitch. This may happen when you restarted the program to quickly."
						"The program will now exit.")
			exit()

		if buffer is not None:

			if show_chat is True:
				buffer_split = buffer.split()

				if buffer_split[1] == '001':
					print_info("Successfully logged in.")
				elif buffer_split[1] == 'JOIN':
					print_info("Joining channels...")
				elif buffer_split[1] == 'PRIVMSG':
					irc_string = ""

					#Get Username from first split and store it
					username = buffer_split[0][1:].split('!')[0]

					buffer_split = buffer_split[2:]
					irc_string += buffer_split.pop(0)
					irc_string += " {}: ".format(username)

					#Remove Colon from first Chat Word
					irc_string += "{} ".format(buffer_split.pop(0)[1:])

					for element in buffer_split:
						irc_string += element + " "
					print(bcolors.LIGHT_WHITE + irc_string)


			resp, buffer = buffer.split('\n', 1)
			if resp.startswith('PING'):
				send(socket, "PONG", "")
				print(bcolors.PURPLE + "Pong send")
			resplit = resp.strip().split()

			if resplit[1] == "PRIVMSG":
				try:
					msg = resp.strip().split(":", 2)  # split(":", 2)
					msg_split = msg[2].split(" ")
					channel_privmsg = msg[1].split("PRIVMSG")[1].strip()
					user = msg[1].split("!")[0]
				except:
					print("Error while resplitting:\n=============")
					print("msg:\n{}\n=============".format(msg))
					print("resp:\n{}".format(resp))
					# TODO: Error-Log to file
					continue

				if msg_split[0] == "funnymomentspog":
					print(bcolors.GREEN + "Channel: {} => {}".format(channel_privmsg, msg_split[0]))

				elif msg_split[0] == "!raffle":
					print(bcolors.GREEN + "Channel: {} => !raffle".format(channel_privmsg))
					if is_live(channel_privmsg) is True:
						if is_owner(channel_privmsg, user) is True:
							sleep(10)
							print(bcolors.BLUE + "BOT: Send '!join' to Channel: {}".format(channel_privmsg))
							answer(socket, channel_privmsg, '!join')
						elif is_owner(channel_privmsg, user) is False:
							print(bcolors.RED + "---")
					elif is_live(channel_privmsg) is False:
						print(bcolors.GREEN + "BOT: {} tried to fool us :P".format(channel_privmsg))


def is_live(channel_privmsg):
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
		print(bcolors.GREEN + "User: {} is not owner. \n {} tried to fool us !!!!".format(user, user))
		return False


if __name__ == "__main__":
	try:
		init_update()
		print_banner()

		config = get_config()
		data = get_data()
		show_chat = get_show_chat()
		socket = connect()

		print_spacer()

		print("Debug: Entering loop...")
		loop()

	except KeyboardInterrupt:
		print(bcolors.YELLOW + "\nProgram closed by user (CTRL+C)")
		exit()