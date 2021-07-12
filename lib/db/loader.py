import json
import os

config_file = open('lib/db/config/config.json')
config = json.load(config_file)

try:
	try:

		if config['quickstart']:
			os.system("python3 lib/db/debug.py")
		elif not config['quickstart']:
			os.system("python3 lib/db/main.py")

	except KeyError:

		session = input("Want to start debug session? [y/n]")
		if session == "y" or session == "Y":
			os.system("python3 lib/db/debug.py")
		else:
			os.system("python3 lib/db/main.py")
except KeyboardInterrupt:
	print("\nProgram closed by user (CTRL+C)")
	exit()