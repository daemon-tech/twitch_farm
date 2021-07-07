import json
import requests
import argparse
import time
import os
import subprocess

subprocess.call('clear', shell=True)

#Check dependencies

def check_colors():
    try:
        from moduels.colors import  *
    except:
        print("DEBUG: modules/colors.py missing")
        git_pull_install = input("Install? [y/n]")
        if git_pull_install == "y" or git_pull_install = "Y":
            os.system("git pull")
            check_colors()
        else:
            close()

if __name__ == "__main__":
    check_colors()
#code    
