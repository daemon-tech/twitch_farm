import os
import subprocess

#check modules
def load():
	os.system("clear")

	try:
		from lib.db.modules.colors import bcolors
	except ModuleNotFoundError:
		print("lib/db/modules/colors.py seems missing. Did you install this program correctly?")
		exit()
	except ImportError:
		print("lib/db/modules/colors.py seems to exist, but is corrupted. Did you install this program correctly?")
		exit()

	try:
		import pyfiglet
	except ModuleNotFoundError:
		if os.name != "nt":
			os.system("python3 -m pip install pyfiglet==0.7")
			load()
		else:
			exit()
	try:
		import json
		import time
		import sys
	except ModuleNotFoundError:
		print("Some Modules are not correctly installed.\n json;time;sys")
		install = input("Want to install now? [y/n]")
		if install == "y" or install == "Y":
			if os.name != "nt":
				os.system("apt install python3.7")
				os.system("python3 -m pip install json")
				os.system("python3 -m pip install time")
				os.system("python3 -m pip install sys")
				load()
			else:
				exit()
		else:
			exit()


def start_main():
	# Needs to be imported in start_main() to ensure previous ModuleNotFoundError-check
	import json

	try:
		config_file = open('lib/db/config/config.json')
		config = json.load(config_file)

		if config['quickstart']:
			os.system("python3 lib/db/loader.py")
		elif not config['quickstart']:
			start_menue()

	except FileNotFoundError:
		print('"config.json" not found. Please configure "example.json" and rename it to "config.json".')
		exit()
	except json.decoder.JSONDecodeError as err:
		print("Unable to read JSON File:\n" + format(err))
		exit()
	except KeyError:
		start_menue()


def start_menue():
	print("Modules correctly installed. Starting session?")
	start = input("[y/n]")
	if start == "y" or start == "Y":
		os.system("python3 lib/db/loader.py")



if __name__ == "__main__":
	try:
		load()
		start_main()
	except KeyboardInterrupt:
		print("\nProgram closed by user (CTRL+C)")
		exit()