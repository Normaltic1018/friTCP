# Windows Program Frida DBI
import frida
import sys, os
version = 0.3

commands = {"proxy":"capture the api in capture_list",
"set":"Set Options",
"exit":"Exit This Script"}

settings_validation = {"mode":["hex", "string"],
"capture_list":["send","recv","wsasend","wsarecv","recvfrom","wsarecvfrom"]
}

settings = {"mode":"string",
"capture_list":["send","recv"]
}

hook_function_script = """
	var hook_module_name = "WS2_32.dll";
	var hook_function_name = "send";
	var hookPtr = Module.findExportByName(hook_module_name, hook_function_name);
	send(hook_function_name +' address:' + hookPtr.toString());
	
	Interceptor.attach(hookPtr,{
		onEnter: function(args){
			send(hook_function_name+' Called');
			send('buf:' + Memory.readCString(args[1]));
			var data_len = args[2];
			send('buf count:' + data_len);
			var user_write_data;
			send("interactive");
			var op = recv('input',function(value){
				user_write_data = value.payload;
			});
			op.wait();
			Memory.writeAnsiString(args[1], user_write_data);
			send('Modified buf:' + Memory.readCString(args[1]));
			//send(hook_function_name+' called From:' + Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join("\\n") + " ");
		},
		onLeave: function (retval){
		}
	});
"""

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
		
	

      

def get_script(script_name):
	with open('js_script\\'+script_name, 'r') as f:
		script = f.read()
	return script

def validate_setting(mode, value):
	if value in settings_validation[mode]:
		return True

	return False

def main(target_process):
	
	global script
	session = frida.attach(target_process)
   
	show_banner()
	while True:
		cmd = shell_loop()
      		
		if cmd == 'proxy':
			if len(settings['capture_list']) != 0 :
				for capture_api in settings['capture_list']:
					script = session.create_script(get_script('func_proxy.js') % (capture_api, settings["mode"]))
					script.on('message', on_input_message)
					script.load()
			else:
				print("#>Empty capture_list...")
				print("#>Please Set capture_list")
				print("")
		elif cmd == 'clear' or cmd == 'cls':
			os.system('cls')
		elif cmd.startswith("set"):
			cmd = cmd.split()
			if len(cmd) > 1 :
				if cmd[1] in settings:
					if cmd[1] == "capture_list":
						list_num = len(cmd) - 2
						new_api_list = []
						for i in range(list_num):
							if(validate_setting(cmd[1], cmd[2+i])):
								new_api_list.append(cmd[2+i])
							else:
								print("This is not API [{}]".format(cmd[2+i]))
						
						if len(new_api_list) != 0:
							settings[cmd[1]] = new_api_list
							print("#>Apply Complete!")
							print("")
							show_current_settings()
						else:
							print("#>Not Changed...")
					else:
						if(validate_setting(cmd[1],cmd[2])):
							settings[cmd[1]] = cmd[2]
							print("#>Apply Complete!")
							print("")
							show_current_settings()
						else:
							print("#>Wrong Value, Check Your Command")
				else:
					print("#>Wrong Value, Check Your Command")
					show_settings()
			else:
				os.system('cls')
				show_settings()
		elif cmd == 'exit':
			print('Good Bye~')
			sys.exit()
            
	#sys.stdin.read()

def on_message(message, data):
	if message['type'] == 'send':
		print(message['payload'])
	elif message['type'] == 'error':
		print(message['stack'])
		
def on_input_message(message, data):
	#print(message)
	if message['type'] == 'send':
		if(message['payload'] == "interactive"):
			user_input = input("Data : ")
			script.post({'type':'input','payload':user_input})
		else:
			print(message['payload'])
	elif message['type'] == 'error':
		print(message['stack'])
		
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage : %s <process name or PID>' % __file__)
		sys.exit(1)
   
	try:
		target_process = int(sys.argv[1])
	except:
		target_process = sys.argv[1]
         
   
	main(target_process)