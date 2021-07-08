import json
import time
import os
import subprocess
import pyfiglet
import sys

from pyfiglet import Figlet
from socket import *

subprocess.call('clear', shell=True)

#Check dependencies
def init_update():
    try:
        os.system("git pull")
    except:
        pass

def check_color():
	try:
		from modules.colors import bcolors
	except:
		print(f"DEBUG: modules/colors.py missing")
		exit()
		
def banner():
	from modules.colors import bcolors
	title = Figlet(font="banner3-D")
	print(bcolors.PURPLE + title.renderText("TFARMER"))

if __name__ == "__main__":
    init_update()
    check_color()
    banner()
