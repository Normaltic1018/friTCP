# Windows Program Frida DBI
import frida
import sys, os
from tcp_proxy_core.tcp_proxy_config import *
from tcp_proxy_interface import dev_interface as dev
from tcp_proxy_interface import gui_interface as gui
from tcp_proxy_core.core_func import *

def main(target_process):
	
	
	session = frida.attach(target_process)
   
	#dev.show_banner()
	gui.print_info()
	while True:
		#cmd = dev.shell_loop()
		cmd = gui.get_cmd()
      		
		if cmd == 'proxy':
			if len(settings['capture_list']) != 0 :
				for capture_api in settings['capture_list']:
					hook_api(session,capture_api)
			else:
				gui.print_error("Empty capture_list")
		elif cmd == 'clear' or cmd == 'cls':
			os.system('cls')
		elif cmd.startswith("set"):
			set_cmd(cmd)
		elif cmd == 'exit':
			#dev.exit_message()
			sys.exit()
            
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