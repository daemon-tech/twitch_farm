import json
import os

config_file = open('lib/db/config/config.json')
config = json.load(config_file)

try:

	if config['debug']:
		os.system("python3 lib/db/debug.py")
	elif not config['debug']:
		os.system("python3 lib/db/main.py")

except KeyError:

	try:
		session = input("Want to start debug session? [y/n]")
		if session == "y" or session == "Y":
			os.system("python3 lib/db/debug.py")
		else:
			os.system("python3 lib/db/main.py")
	except KeyboardInterrupt:
		print("\nProgram closed by user (CTRL+C)")
		exit()