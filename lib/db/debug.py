import json
import os
from pyfiglet import Figlet
from random import randint
import re
import requests
import subprocess
import socket
import sys
from time import sleep

from modules.colors import bcolors


SERVER = 'irc.twitch.tv'
PORT = 6667
IGNORED_COMMANDS = ['002', '003', '004', '366', '372', '375', '376', 'JOIN']

subprocess.call('clear', shell=True)


def init_update():
	if os.path.basename(__file__) == 'main.py':
		print_debug('Filename is main.py, attempting auto-update...')
		# TODO: Auto-Update using Git
	else:
		print_debug('Filename is debug.py, skipping auto-update.')


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
	try:
		if config['debug']:
			print("{}DEBUG: {}".format(bcolors.CYAN, debug_string))
	except KeyError:
		pass


# =====================================================================================================================
# DATA


def get_config():
	# Error Handling already happened in launcher
	config_file = open('lib/db/config/config.json')

	return json.load(config_file)


def get_credentials():
	username=''
	token=''

	try:
		username = config['credentials']['username']
		token = config['credentials']['token']
	except KeyError:
		print_error("Credentials not exist or are entered incorrectly. Program will now exit.")
		exit()

	print_debug('Username is {}'.format(username))
	if not token.startswith('oauth:'):
		print_debug('Token did not start with "oauth:". Prepended it...')
		token = 'oauth:{}'.format(token)
	print_debug('Token ends with {}'.format(token[:3]))

	return [username, token]


# =====================================================================================================================
# Connection


def connect():

	print_debug('Establishing socket connection towards {}:{}...'.format(SERVER, PORT))
	irc_socket = socket.socket()
	irc_socket.connect((SERVER, PORT))

	sock_token = "PASS {}\r\n".format(credentials[1])
	sock_username = "NICK {}\r\n".format(credentials[0])
	irc_socket.send(sock_token.encode("utf-8"))
	irc_socket.send(sock_username.encode("utf-8"))

	for channel in config['channels']:
		sock_channel = "JOIN #{}\r\n".format(channel.lower())
		print_debug('Requesting to join channel #{}...'.format(channel))
		irc_socket.send(sock_channel.encode("utf-8"))

	return irc_socket


def receive(irc_socket, buffer_size):
	return irc_socket.recv(buffer_size).decode("utf-8")


def send(irc_socket, command, message):
	irc_command = "{} {}".format(command, message)
	print_debug('Sending command {}'.format(irc_command))
	irc_socket.send('{}\r\n'.format(irc_command).encode("utf-8"))


def answer(irc_socket, channel, message):
	irc_message = "PRIVMSG {} :{}".format(channel, message)
	print_debug('Sending message {}'.format(irc_message))
	irc_socket.send('{}\r\n'.format(irc_message).encode("utf-8"))


# =====================================================================================================================
# Core


def loop(irc_socket):
	buffer_size = 4096
	buffer = ''
	while True:
		while True:
			try:
				buffer += receive(irc_socket, buffer_size)
			except ConnectionResetError:
				print_error("Connection was reset by Twitch. This may happen when you restarted the program to quickly."
							"Waiting a few seconds to attempt restart...")
				sleep(5)
				os.execv(sys.argv[0], sys.argv)
			break

		if buffer is not None:
			responses = buffer.split("\r\n")
			print_debug('responses:\n{}\n'.format(responses))

			for i, response in enumerate(responses):
				# if not last response in responses:
				if not i == len(responses)-1:
					# remove response from buffer
					buffer = buffer[len(response)+2:]
					response_split = response.split()
					print_debug('response_split: {}'.format(response_split))

					if response_split:
						# if not starting with ":" and ending with "tmi.twitch.tv" (Begin of a new IRC message):
						if not re.match('^:.*tmi\.twitch\.tv', response_split[0]):
							# [PING, SERVER]
							if response_split[0] == 'PING':
								send(socket, "PONG", "")
								print_info("Pong Send.")
							else:
								buffer_size *= 2
								print_info('Buffer-size exhausted. Increasing to {}...'.format(buffer_size))
								buffer = ''
						else:
							evaluate_response(response_split)


def evaluate_response(response_split):
	#[SERVER, 001, username, welcome message]
	if response_split[1] == '001':
		print_info("Login successful.")
	#[username.server, JOIN, channel]
	elif response_split[1] == '353':
		print_info("Joined channel {}.".format(response_split[4]))
	#[username.server, PRIVMSG, channel, :message, ...]
	elif response_split[1] == 'PRIVMSG':
		channel = response_split[2]
		author = response_split[0][1:].split('!')[0]
		message = parse_message(response_split)
		print_debug('message: {}'.format(message))
		evaluate_message(channel, author, message)
	elif response_split[1] in IGNORED_COMMANDS:
		print_debug('Ignored response.')
	else:
		pass
		# TODO Log this shit



def parse_message(response_split):
	# Remove /me or the Column at the first word
	if response_split[3] == ':\x01ACTION':
		print_debug('Message included formatting using /me. Cleaning up...')
		message = response_split[4:]
		message[len(message) - 1] = message[len(message) - 1][:-1]
	else:
		message = response_split[3:]
		message[0] = message[0][1:]
	return message


def evaluate_message(channel, author, message):
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
		if author == credentials[0]:
			print_chat(bcolors.YELLOW, channel, author, message)
			print("{}Successfully joined raffle in {}! Good luck!".format(bcolors.LIGHT_GREEN, channel))
	else:
		try:
			if config['show_chat'] is True:
				print_chat(bcolors.WHITE, channel, author, message)
		except KeyError:
			print_error(
				"Can't find 'show_chat' configuration. Is your config.json corrupted? Program will now exit.")
			exit()


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
		config = get_config()
		init_update()
		print_banner()

		credentials = get_credentials()
		socket = connect()

		print_spacer()

		loop(socket)

	except KeyboardInterrupt:
		print(bcolors.YELLOW + "\nProgram closed by user (CTRL+C)")
		exit()
