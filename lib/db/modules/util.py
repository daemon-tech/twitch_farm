import datetime
from pyfiglet import Figlet

from .colors import BColors
from .config import Config

def print_banner():
	print(BColors.PURPLE + Figlet(font='banner3-D').renderText('TFARMER'))

def print_spacer():
	print(BColors.WHITE + "\n\n\n :::..:::::..::::::::..:::::..::..:::::..::..:::::..::........::..:::::..::\n")


# Print Info Function Lambda
print_info = lambda info_string:\
	print("{}{}[INFO]  {}{}".format(timestamp(), BColors.PURPLE, BColors.WHITE, info_string))


# Print Error Function Lambda
print_error = lambda err_string:print("{}{}[ERROR] {}".format(timestamp(), BColors.RED, err_string))


# Print Debug Function Lambda
print_debug = lambda debug_string:\
	[print("{}{}[DEBUG] {}".format(timestamp(), BColors.CYAN, debug_string))
	 if Config.CONFIG_OBJECT['debug'] else print("", end="")]


def timestamp():
	x = datetime.datetime.now()
	return x.strftime('{}[%d.%m.%y %H:%M:%S]'.format(BColors.PURPLE))