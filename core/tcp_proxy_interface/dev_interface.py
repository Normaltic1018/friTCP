import os
from tcp_proxy_core.tcp_proxy_config import *

def shell_loop():
	cmd = input('#>')
	return cmd

def show_current_settings():
	print("## Current Settings")
	
	for setting in settings:
		print("{} ---> {}".format(setting,settings[setting]))


def show_settings():
	print("#"*52 + "\n")
	print("Setting Usage")
	print("#>set [setting] [value]")
	print("Ex) set mode hex")
	print("")
	show_current_settings()

	print("\n"+"#"*52)
	

def show_banner():
	banner = """
##########################################################

TCP_PROXY_NORMALTIC (PRIMITIVE)
version : {}
Made by Normaltic

##########################################################
""".format(version)

	os.system("cls")
   
	print(banner)
   
	print("[ Settings ]")
	
	for setting in settings:
		print("{} ---> {}".format(setting,settings[setting]))
		
	print("")
	
	print("[ Command ]")
	for command in commands:
		print("{} ---> {}".format(command,commands[command]))
		
	
def exit_message():
	print("exit... Good Bye!")
