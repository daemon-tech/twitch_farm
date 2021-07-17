import datetime
from pyfiglet import Figlet

from .colors import BColors

def print_banner():
	title = Figlet(font="banner3-D")
	print(BColors.PURPLE + title.renderText("TFARMER"))

def print_spacer():
	print(" ")
	print(" ")
	print(BColors.WHITE + ":::..:::::..::::::::..:::::..::..:::::..::..:::::..::........::..:::::..::")
	print(" ")

def print_info(info_string):
	print("{}{}[INFO]  {}{}".format(timestamp(), BColors.PURPLE, BColors.WHITE, info_string))

def print_error(err_string):
	print("{}{}[ERROR] {}".format(timestamp(), BColors.RED, err_string))

def print_debug(debug_string, config):
	try:
		if config['debug']:
			print("{}{}[DEBUG] {}".format(timestamp(), BColors.CYAN, debug_string))
	except KeyError:
		pass


def timestamp():
	x = datetime.datetime.now()
	return x.strftime('{}[%d.%m.%y %H:%M:%S]'.format(BColors.PURPLE))