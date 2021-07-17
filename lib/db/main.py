import json
import os
import requests
import sys
from time import sleep
from threading import Thread

from modules.colors import BColors
from modules import connection
from modules.connection import IRCSocket
from modules import util


SERVER = 'irc.twitch.tv'
PORT = 6667
IGNORED_COMMANDS = ['002', '003', '004', '366', '372', '375', '376', 'JOIN']

global TIMEOUT

os.system("clear")


# =====================================================================================================================
# DATA GATHERING


def get_config():
	# Error Handling already happened in launcher
	config_file = open('lib/db/config/config.json')

	return json.load(config_file)


def get_credentials():
	username_= ''
	token_=''

	try:
		username_ = config['credentials']['username']
		token_ = config['credentials']['token']
	except KeyError:
		util.print_error("Credentials not exist or are entered incorrectly. Program will now exit.")
		exit()

	util.print_debug('Username is {}'.format(username_), config)
	if not token_.startswith('oauth:'):
		util.print_debug('Token did not start with "oauth:". Prepended it...', config)
		token_ = 'oauth:{}'.format(token_)
	util.print_debug('Token ends with {}'.format(token_[:3]), config)

	return [username_, token_]


def get_sets():
	channel_set_ = set()
	channel_color_dict_ = dict()
	user_set_ = set()
	word_set_ = set()

	try:
		for channel in config['channels']:
			try:
				if config['show_chat']:
					try:
						if config['channels'][channel]['show_chat']:
							add_channel_color(channel, channel_set_, channel_color_dict_)
					except KeyError:
						util.print_info('Missing key "show_chat" for channel {} in config.json.'
								   'Assumes "True"...'.format(channel))
						add_channel_color(channel, channel_set_, channel_color_dict_)
			except KeyError:
				util.print_error("Can't find global 'show_chat' key. Is your config.json corrupted? Program will now exit.")
				exit()
	except KeyError:
		util.print_error('Could not find key "channels". Is your config.json corrupted?'
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


def add_channel_color(channel, channel_set_, channel_color_dict_):
	channel_set_.add(channel.lower())
	try:
		if config['channels'][channel]['channel_color']:
			try:
				channel_color_dict_[channel.lower()] = eval('BColors.{}'
															.format(config['channels'][channel]['channel_color']))
			except AttributeError:
				raise KeyError
	except KeyError:
		channel_color_dict_[channel.lower()] = ''


# =====================================================================================================================
# CORE


def loop(irc_socket):
	buffer = b''
	while True:
		while True:
			try:
				buffer += irc_socket.receive()
				util.print_debug('buffer:\n{}\n'.format(buffer), config)
			except ConnectionResetError:
				util.print_error("Connection was reset by Twitch. This may happen when you restarted the program to quickly."
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
			util.print_debug('responses:\n{}\n'.format(responses), config)

			for i, response in enumerate(responses):
				# if not last response in responses:
				if not i == len(responses)-1:
					# remove response from buffer_decoded
					buffer = buffer[len(response.encode('utf-8'))+2:]
					response_split = response.split()
					util.print_debug('response_split: {}'.format(response_split), config)
					evaluate_response(response_split, irc_socket)


def evaluate_response(response_split, irc_socket):
	# [PING, SERVER]
	if response_split[0] == 'PING':
		global TIMEOUT
		TIMEOUT = 300
		irc_socket.send("PONG", "", config)
		util.print_info("Pong Send.")
	#[SERVER, 001, username, welcome message]
	elif response_split[1] == '001':
		util.print_info("Login successful.")
	#[username.server, JOIN, channel]
	elif response_split[1] == '353':
		util.print_info("Joined channel {}.".format(response_split[4]))
	#[username.server, PRIVMSG, channel, :message, ...]
	elif response_split[1] == 'PRIVMSG':
		channel = response_split[2]
		author = response_split[0][1:].split('!')[0]
		message = parse_message(response_split)
		util.print_debug('message: {}'.format(message), config)
		evaluate_message(channel, author, message, irc_socket)
	elif response_split[1] in IGNORED_COMMANDS:
		util.print_debug('Ignored response.', config)
	else:
		util.print_error('Found Unknown IRC Command with Status-Code {}. If you see this message, please report this'
					'accident to the developers.\nresponse_split: {}'.format(response_split[1], response_split))



def parse_message(response_split):
	# Remove /me or the Column at the first word
	if response_split[3] == ':\x01ACTION':
		util.print_debug('Message included formatting using /me. Cleaning up...', config)
		message = response_split[4:]
		message[len(message) - 1] = message[len(message) - 1][:-1]
	else:
		message = response_split[3:]
		message[0] = message[0][1:]
	return message


def evaluate_message(channel, author, message, irc_socket):
	if message[0] == "funnymomentspog":
		connection.print_chat(BColors.GREEN, channel, author, message)
	elif message[0] == "!sraffle" or message[0] == "!raffle":
		if channel[1:] == author:
			if is_live(channel):
				connection.print_chat(BColors.PURPLE, channel, author, message)
				util.print_info("{}Valid Raffle detected in {}! Trying to participate..."
						   .format(BColors.LIGHT_GREEN, channel))
				s = Thread(target=irc_socket.send_random, args=(30, 55, channel, '!join'))
				s.daemon = True
				s.start()
			else:
				util.print_info("{} tried to launch a raffle, but he is currently offline!".format(author))
		else:
			util.print_info("{} tried to launch a raffle in {}!".format(author, channel))
	else:
		if config['show_chat'] is True:
			if channel[1:] in channel_set:
				if not message[0].lower() in word_set:
					if not author in user_set:
						if not channel_color_dict[channel[1:]] == '':
							connection.print_chat_c_color(
								channel_color_dict[channel[1:]], channel, BColors.WHITE, author, message)
						else:
							connection.print_chat(BColors.WHITE, channel, author, message)
					else:
						util.print_debug('Message was by ignored user. Skipping...', config)
				else:
					util.print_debug('Message started with an ignored word. Skipping...', config)


def is_live(channel):

	thumbnail = requests.get("https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-1x1.jpg".format(channel[1:]))
	if format(thumbnail.history) == '[]':
		return True
	elif format(thumbnail.history) == '[<Response [302]>]':
		return False
	else:
		util.print_error("Unknown Status Code when checking thumbnail:\n{}\nThe raffle was skipped as security measurement."
					.format(format(thumbnail.history)))


# ====================================================================================================================
# MAIN

if __name__ == "__main__":
	try:
		config = get_config()
		username, token = get_credentials()
		channel_set, user_set, word_set, channel_color_dict = get_sets()
		util.print_banner()

		IRCSocket = IRCSocket(SERVER, PORT, username, token, config)
		util.print_debug('Entered Watchdog.', config)
		wd = Thread(target=connection.watchdog, args=(config,))
		wd.daemon = True
		wd.start()
		util.print_debug('Left Watchdog', config)
		util.print_spacer()

		loop(IRCSocket)

	except KeyboardInterrupt:
		print(BColors.YELLOW + "\nProgram closed by user (CTRL+C)")
		exit()
