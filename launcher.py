import os
import subprocess

#check modules
def load():
    subprocess.call('clear', shell=True)
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
        print("SomeModules are not correctly installed.\n json;requests;argparser;time")
        install = input("Want to install now? [y/n]")
        if install == "y" or install == "Y":
            if os.name != "nt":
                os.system("apt install python3.7")
                os.system("python3 -m pip install argparse")
                load()
            else:
                exit()
        else:
            exit()

def start_main():
    print("Modules correctly installed. Starting session?")
    start = input("[y/n]")
    if start == "y" or start == "Y":
        os.system("python3 lib/db/loader.py")

if __name__ == "__main__":
	load()
	start_main()
