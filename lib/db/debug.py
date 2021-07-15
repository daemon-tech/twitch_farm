import datetime
import json
import os
from pyfiglet import Figlet
from random import randint
import requests
import socket
import sys
from time import sleep
from threading import Thread

from modules.colors import bcolors


SERVER = 'irc.twitch.tv'
PORT = 6667
IGNORED_COMMANDS = ['002', '003', '004', '366', '372', '375', '376', 'JOIN']


global TIMEOUT


command = lambda x: os.system(x)
command("clear")


closing = lambda string: print(bcolors.YELLOW + "\n{}".format(string))


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
	print("{}{}[INFO]  {}{}".format(timestamp(), bcolors.PURPLE, bcolors.WHITE, info_string))

def print_error(err_string):
	print("{}{}[ERROR] {}".format(timestamp(), bcolors.RED,  err_string))

'''def print_debug(debug_string):
	try:
		if config['debug_output']:
			print("{}{}[DEBUG] {}".format(timestamp(), bcolors.CYAN,  debug_string))
	except KeyError:
		pass'''


print_debug = lambda debug_string: [print("{}{}[DEBUG] {}".format(timestamp(), bcolors.CYAN,  debug_string))] if not config['debug_output'] else print('ERROR: L56')


def timestamp():
	x = datetime.datetime.now()
	return x.strftime('{}[%d.%m.%y %H:%M:%S]'.format(bcolors.PURPLE))


# =====================================================================================================================
# DATA


def get_config():
	#Error Handling already happened in launcher
	config_file = open('lib/db/config/config.json')

	return json.load(config_file)

def get_credentials():
	username = ''
	token = ''

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


def get_sets():
	channel_set_ = set()
	channel_color_dict_ = dict()
	user_set_ = set()
	word_set_ = set()

	try:
		for channel in config['channels']:
			try:
				if config['show_chat']:
					# Using the channel loop to create a list of all channels which allow
					try:
						if config['channels'][channel]['show_chat']:
							channel_show(channel, channel_set_, channel_color_dict_)
					except KeyError:
						print_info('Missing key "show_chat" for channel {} in config.json.'
								   'Assumes "True"...'.format(channel))
						channel_show(channel, channel_set_, channel_color_dict_)
			except KeyError:
				print_error("Can't find global 'show_chat' key. Is your config.json corrupted? Program will now exit.")
				exit()
	except KeyError:
		print_error('Could not find key "channels". Is your config.json corrupted?'
					'The program will now exit.')
		exit()

	try:
		for user in config['ignored_users']:
			user_set_.add(user.lower())
	except KeyError:
		pass

	try:
		for word in config['ignored_words']:
			word_set_.add(word.lower())
	except KeyError:
		pass

	return channel_set_, user_set_, word_set_, channel_color_dict_


def channel_show(channel, channel_set_, channel_color_dict_):
	channel_set_.add(channel.lower())
	try:
		if config['channels'][channel]['channel_color']:
			try:
				channel_color_dict_[channel.lower()] = eval('bcolors.{}'
															.format(config['channels'][channel]['channel_color']))
			except AttributeError:
				raise KeyError
	except KeyError:
		channel_color_dict_[channel.lower()] = ''


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


def receive(irc_socket):
	return irc_socket.recv(4096)


def send(irc_socket, command, message):
	irc_command = "{} {}".format(command, message)
	print_debug('Sending command {}'.format(irc_command))
	irc_socket.send('{}\r\n'.format(irc_command).encode("utf-8"))


def answer(irc_socket, channel, message):
	irc_message = "PRIVMSG {} :{}".format(channel, message)
	print_debug('Sending message {}'.format(irc_message))
	irc_socket.send('{}\r\n'.format(irc_message).encode("utf-8"))

def connectivity():
	global TIMEOUT
	TIMEOUT = 300
	while True:
		sleep(1)
		TIMEOUT -= 1
		print_debug('TIMEOUT: {}'.format(TIMEOUT))
		if TIMEOUT == 0:
			print_error("Lost connection to the socket. Waiting a few seconds to attempt restart...")
			sleep(5)
			os.execv(sys.executable, ['python3'] + [os.path.abspath(sys.argv[0])])



# =====================================================================================================================
# Core


def loop(irc_socket):
	buffer = b''
	while True:
		while True:
			try:
				buffer += receive(irc_socket)
				print_debug('buffer:\n{}\n'.format(buffer))
			except ConnectionResetError:
				print_error("Connection was reset by Twitch. This may happen when you restarted the program to quickly."
							" Waiting a few seconds to attempt restart...")
				sleep(5)
				os.execv(sys.executable, ['python3'] + [os.path.abspath(sys.argv[0])])
			try:
				buffer_decoded = buffer.decode('utf-8')
				break
			except UnicodeDecodeError:
				#An unicode symbol was split over 2 different buffers. Keep current buffer and receive again.
				pass

		if buffer_decoded is not None:
			responses = buffer_decoded.split("\r\n")
			print_debug('responses:\n{}\n'.format(responses))

			for i, response in enumerate(responses):
				# if not last response in responses:
				if not i == len(responses)-1:
					# remove response from buffer_decoded
					buffer = buffer[len(response.encode('utf-8'))+2:]
					response_split = response.split()
					print_debug('response_split: {}'.format(response_split))
					evaluate_response(response_split)


def evaluate_response(response_split):
	# [PING, SERVER]
	if response_split[0] == 'PING':
		global TIMEOUT
		TIMEOUT = 300
		send(socket, "PONG", "")
		print_info("Pong Send.")
	#[SERVER, 001, username, welcome message]
	elif response_split[1] == '001':
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
		print_error('Found Unknown IRC Command with Status-Code {}. If you see this message, please report this'
					'accident to the developers.\nresponse_split: {}'.format(response_split[1], response_split))



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
	elif message[0] == "!sraffle" or message[0] == "!raffle":
		if channel[1:] == author:
			if is_live(channel):
				print_chat(bcolors.PURPLE, channel, author, message)
				print_info("{}Valid Raffle detected in {}! Trying to participate..."
					  .format(bcolors.LIGHT_GREEN, channel))
				s = Thread(target=send_random, args=(30, 55, channel, '!join'))
				s.daemon = True
				s.start()
			else:
				print_info("{} tried to launch a raffle, but he is currently offline!".format(author))
		else:
			print_info("{} tried to launch a raffle in {}!".format(author, channel))
	else:
		if config['show_chat'] is True:
			if channel[1:] in channel_set:
				if not message[0].lower() in word_set:
					if not author in user_set:
						if not channel_color_dict[channel[1:]] == '':
							print_chat_c_color(channel_color_dict[channel[1:]], channel, bcolors.WHITE, author, message)
						else:
							print_chat(bcolors.WHITE, channel, author, message)
					else:
						print_debug('Message was by ignored user. Skipping...')
				else:
					print_debug('Message started with an ignored word. Skipping...')


def print_chat_c_color(channel_color, channel, color, author, message):
	irc_string = "{}{} {} {}{}: ".format(timestamp(), channel_color, channel, color, author)
	for element in message:
		irc_string += element + " "
	print(irc_string)

def print_chat(color, channel, author, message):
	irc_string = "{} {}{} {}: ".format(timestamp(), color, channel, author)
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


def send_random(early, late, channel, message):
	sleep(randint(early, late))
	answer(socket, channel, message)
	print_chat(bcolors.LIGHT_GREEN, channel, credentials[0], message)


# ====================================================================================================================
# Main

if __name__ == "__main__":
	try:
		config = get_config()
		init_update()
		print_banner()

		credentials = get_credentials()
		channel_set, user_set, word_set, channel_color_dict = get_sets()
		socket = connect()
		c = Thread(target=connectivity)
		c.daemon = True
		c.start()

		print_spacer()
		loop(socket)

	except KeyboardInterrupt:
		closing("Program closed by user (CTRL+C)")
		#print(bcolors.YELLOW + "\nProgram closed by user (CTRL+C)")
		exit()
