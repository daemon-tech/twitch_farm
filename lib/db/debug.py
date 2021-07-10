import json
import os
from pyfiglet import Figlet
from random import randint
import requests
import subprocess
import socket
from time import sleep

from modules.colors import bcolors



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
	print(bcolors.WHITE + ":::..:::::..::::::::..:::::..::..:::::..::..:::::..::........::..:::::..::")
	print(" ")

def print_info(info_string):
	print("{}INFO:{} {}".format(bcolors.PURPLE, bcolors.WHITE, info_string))

def print_error(err_string):
	print("{}ERROR: {}".format(bcolors.RED, err_string))

def print_debug(debug_string):
	print("{}DEBUG:\n{}".format(bcolors.CYAN, debug_string))


# =====================================================================================================================
# DATA


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
		print_error("Credentials not exist or are entered incorrectly. Program will now exit.")
		exit()

	server = 'irc.chat.twitch.tv'
	port = 6667

	return [username, token, server, port]


def get_show_chat():
	try:
		return config['show_chat']
	except KeyError:
		print_error("Can't find 'show_chat' configuration. Is your config.json corrupted? Program will now exit.")
		exit()


# =====================================================================================================================
# Connection


def connect():

	irc_socket = socket.socket()
	irc_socket.connect((data[2], data[3]))
	sock_token = "PASS {}\n".format(data[1])
	sock_username = "NICK {}\n".format(data[0])

	# Authentification
	irc_socket.send(sock_token.encode("utf-8"))
	irc_socket.send(sock_username.encode("utf-8"))
	for i in config['channels']:
		sock_channel = "JOIN #{}\n".format(i.lower())
		irc_socket.send(sock_channel.encode("utf-8"))
		print_info("Channel: {} joined.".format(i))

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
# Core


def loop():
	while True:
		buffer = ''
		try:
			buffer = receive(socket)
		except ConnectionResetError:
			print_error("Connection was reset by Twitch. This may happen when you restarted the program to quickly."
						"The program will now exit.")
			exit()

		if buffer is not None:
			buffer_split = buffer.split()

			#print_debug(buffer_split)

			if buffer_split[0] == 'PING':
				send(socket, "PONG", "")
				print_info("Pong Send.")
			else:
				channel = buffer_split[2]
				author = buffer_split[0][1:].split('!')[0]

				if buffer_split[1] == 'PRIVMSG':
					message = get_message(buffer_split)

					if message[0] == "funnymomentspog":
						print_chat(bcolors.GREEN, channel, author, message)
					elif message[0] == "!sraffle":
						if channel[1:] == author:
							if is_live(channel):
								print_chat(bcolors.YELLOW, channel, author, message)
								print("{}Valid Raffle detected in {}! Trying to participate..."
									  .format(bcolors.LIGHT_GREEN, channel))
								sleep(randint(30, 55))
								answer(socket, channel, '!join')
							else:
								print_info("{} tried to launch a raffle, but he is currently offline!".format(author))
						else:
							print_info("{} tried to launch a raffle in {}!".format(author, channel))
					elif message[0] == "!join":
						if author == data[0]:
							print_chat(bcolors.YELLOW, channel, author, message)
							print("{}Successfully joined raffle in {}! Good luck!".format(bcolors.LIGHT_GREEN, channel))
					elif show_chat is True:
						print_chat(bcolors.WHITE, channel, author, message)
				elif buffer_split[1] == '001':
					print_info("Login successful.")
				else:
					pass
					# TODO: Log to file


def get_message(buffer_split):
	# Remove /me or the Column at the first word
	if buffer_split[3] == ':\x01ACTION':
		message = buffer_split[4:]
		message[len(message) - 1] = message[len(message) - 1][:-1]
	else:
		message = buffer_split[3:]
		message[0] = message[0][1:]
	return message


def print_chat(color, channel, username, message):
	irc_string = "{}{} {}: ".format(color, channel, username)
	for element in message:
		irc_string += element + " "
	print(irc_string)


def is_live(channel):

	thumbnail = requests.get("https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-1x1.jpg".format(channel[1:]))
	if format(thumbnail.history) == '[]':
		return True
	elif format(thumbnail.history) == '[<Response [302]>]':
		return False
	else:
		print_error("Unknown Status Code when checking thumbnail:\n{}\nThe raffle was skipped as security measurement."
					.format(format(thumbnail.history)))


# ====================================================================================================================
# Main

if __name__ == "__main__":
	try:
		init_update()
		print_banner()

		config = get_config()
		data = get_data()
		show_chat = get_show_chat()
		socket = connect()

		print_spacer()

		loop()

	except KeyboardInterrupt:
		print(bcolors.YELLOW + "\nProgram closed by user (CTRL+C)")
		exit()
