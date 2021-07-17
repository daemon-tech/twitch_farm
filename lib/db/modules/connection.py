from random import randint
from time import sleep
import os
import socket
import sys

from .colors import BColors
from . import util

global TIMEOUT


def watchdog(config):
	global TIMEOUT
	TIMEOUT = 300
	while True:
		sleep(1)
		TIMEOUT -= 1
		util.print_debug('TIMEOUT: {}'.format(TIMEOUT), config)
		if TIMEOUT == 0:
			util.print_error("Lost connection to the socket. Waiting a few seconds to attempt restart...")
			sleep(5)
			os.execv(sys.executable, ['python3'] + [os.path.abspath(sys.argv[0])])


def print_chat_c_color(channel_color, channel, color, author, message):
	irc_string = "{}{} {} {}{}: ".format(util.timestamp(), channel_color, channel, color, author)
	for element in message:
		irc_string += element + " "
	print(irc_string)


def print_chat(color, channel, author, message):
	irc_string = "{} {}{} {}: ".format(util.timestamp(), color, channel, author)
	for element in message:
		irc_string += element + " "
	print(irc_string)


class IRCSocket:
	def __init__(self, server, port, username, token, config):
		util.print_debug('Establishing socket connection towards {}:{}...'.format(server, port), config)
		irc_socket = socket.socket()
		irc_socket.connect((server, port))

		sock_token = "PASS {}\r\n".format(token)
		sock_username = "NICK {}\r\n".format(username)
		irc_socket.send(sock_token.encode("utf-8"))
		irc_socket.send(sock_username.encode("utf-8"))

		for channel in config['channels']:
			sock_channel = "JOIN #{}\r\n".format(channel.lower())
			util.print_debug('Requesting to join channel #{}...'.format(channel), config)
			irc_socket.send(sock_channel.encode("utf-8"))

		self.irc_socket = irc_socket
		self.username = username


	def receive(self):
		return self.irc_socket.recv(4096)


	def send(self, command, message, config):
		irc_command = "{} {}".format(command, message)
		util.print_debug('Sending command {}'.format(irc_command), config)
		self.irc_socket.send('{}\r\n'.format(irc_command).encode("utf-8"))


	def send_random(self, early, late, channel, message):
		sleep(randint(early, late))
		self.answer(socket, channel, message)
		print_chat(BColors.LIGHT_GREEN, channel, self.username, message)


	def answer(self, channel, message, config):
		irc_message = "PRIVMSG {} :{}".format(channel, message)
		util.print_debug('Sending message {}'.format(irc_message), config)
		self.irc_socket.send('{}\r\n'.format(irc_message).encode("utf-8"))
