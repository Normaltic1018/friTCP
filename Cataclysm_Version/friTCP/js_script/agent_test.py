#TEST.py
import frida,sys

def get_script(script_name):
	with open(script_name, 'r') as f:
		script = f.read()
	return script
	
def on_message(message, data):
	if message['type'] == 'send':
		if(message['payload'] == "[AGENT_SHELL]"):
			user_input = input("[Agent shell]#")
			script.post({'type':'shell','payload':user_input})
		else:
			print(message)
	elif message['type'] == 'error':
		print(message['stack'])
		
def main(target_process):
	global script
	session = frida.attach(target_process)
	script = session.create_script(get_script('tcp_proxy_agent.js'))
	script.on('message', on_message)
	script.load()
		        
	#sys.stdin.read()
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage : %s <process name or PID>' % __file__)
		sys.exit(1)
   
	try:
		target_process = int(sys.argv[1])
	except:
		target_process = sys.argv[1]
         
   
	main(target_process)