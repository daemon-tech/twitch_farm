import os

session = input("Want to start debug session? [y/n]")
if session == "y" or session == "Y":
	os.system("python3 lib/db/debug.py")
else:
	os.system("python3 lib/db/main.py")