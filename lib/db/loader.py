import json
import os

config_file = open('lib/db/config/config.json')
debug = json.load(config_file)
try:
	if debug['debug']:
		os.system("python3 lib/db/debug.py")
	elif not debug['debug']:
		os.system("python3 lib/db/main.py")

	#catch missing ErrorHandling "KeyInterrupt" in main/debug.py"
	exit()
except KeyError:
	pass
session = input("Want to start debug session? [y/n]")
if session == "y" or session == "Y":
	os.system("python3 lib/db/debug.py")
else:
	os.system("python3 lib/db/main.py")