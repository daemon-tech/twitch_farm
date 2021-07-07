import os
import subprocess

#check modules
def load():
	subprocess.call('clear', shell=True)
	try:
		import pyfiglet
	except ModuleNotFoundError:
		#if not windows
		if os.name != "nt"
			os.system("python3 -m pip install pyfiglet==0.7")
			load()
		else:
            close()
	try:
		import json
		import requests
		import argparse
		import time
	except ModuleNotFoundError:
		print("SomeModules are not correctly installed.\n json;requests;argparser;time")
		install = input("Want to install now? [y/n]")
		if install == "y" or install == "Y":
            if os.name != "nt"
			os.system("python3 -m pip install argparse)
			load()
        else:
            close()

def start_main():
    print("Modules correctly installed. Starting session?")
    start = input("[y/n]")
    if start == "y" or start == "Y":
        os.system("python3 db/main.py")

if __name__ == "__main__":
	load()