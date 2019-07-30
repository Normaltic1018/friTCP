//Frida Script
var module_list = Process.enumerateModules();
var hook_diction = {};
var input_func_name = "WSARecv";

for(var idx in module_list){
	// Find Function
	var select_module = Process.getModuleByName(module_list[idx].name);
   
	var symbol_list = select_module.enumerateExports();
   
	for(var sym_idx in symbol_list){
		// Compare
		if(symbol_list[sym_idx].name == input_func_name){
			hook_diction[module_list[idx].name] = symbol_list[sym_idx].name;
		}
	}
}  
var call_num = 0;

for(var key in hook_diction){
	var hook_module_name = key;
	var hook_function_name = hook_diction[key];
	
	var hookPtr = Module.findExportByName(hook_module_name, hook_function_name);
	//send("[HOOK_INFO][PID]"+Process.id+" [MODULE]"+hook_module_name+" [FUNCTION]"+hook_function_name+" [ADDRESS]"+ hookPtr.toString());
	
	var buf_ptr;
	
	Interceptor.attach(hookPtr,{
		onEnter: function(args){
			this.sock = args[0];
			this.wsa_buffer_structure = ptr(args[1]);
			this.wsa_buffer_address = Memory.readPointer(this.wsa_buffer_structure.add(4));
			this.wsa_buffer_length = Memory.readULong(this.wsa_buffer_structure);
		},
		onLeave: function(retVal){
			var threadId = Process.getCurrentThreadId();
			if(call_num > 5000){
				call_num = 0;
			}else{
				call_num = call_num + 1;
			}
			console.log("================================= SCRIPT START" + threadId+"_"+call_num);
			send("[KNOCK] [THREAD_ID]"+threadId+"_"+call_num+" [PID]"+Process.id+" [FUNC_NAME]"+hook_function_name);
			var gogo = recv(threadId+"_"+call_num,function(value){
			//console.log("GET POST DATA");
				console.log("GOGO Script");
			});
		
			gogo.wait();
			console.log("================================= SCRIPT RESTART" + threadId);
			console.log("GOGO START");
			var op = recv('input',function(value){
				//console.log("GET POST DATA");
				user_write_data = value.payload;
			});
						
			// i is arg index
			var user_write_data;
			
			// IP, PORT Information
			var socket_fd = this.sock.toInt32();
			var socket_address = Socket.peerAddress(socket_fd);

			// if buf_length is so large, it becomes very slow as it stop...
			//if(buf_length > 4096){buf_length = 4096;}

			var buf_address = this.wsa_buffer_address;
			var buf_length = this.wsa_buffer_length;

			var res = hexdump(buf_address,{offset:0,length:buf_length,header:false,ansi:false});
			
			send("[PROXY]"+"[PID]"+Process.id+" [FUNC_NAME]"+hook_function_name+" [THREAD_ID]"+threadId+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res);
		
			//send("[INTERCEPT]");
			
			// Receive User Data
			op.wait();
								
			var input_len;
			input_len = user_write_data.length;
				
			if(input_len != 0){
				// Hex mode
				user_write_data = user_write_data;
				var list_user_data = user_write_data.split(" ");
				var input_array = new Array();
					
				for(var i in list_user_data){
					input_array[i] = parseInt(list_user_data[i],16);
				}
				input_len = input_array.length;
				input_array.splice(input_len-1,1);
				
				Memory.writeByteArray(this.buf,input_array);
				input_len = input_array.length;
					
				// fill zero if input_length is longer than origin length
				if(input_len < buf_length){
					var null_array = new Array();
					for(var i = 0; i<(buf_length-input_len); i++){null_array[i] = 0;}
						
					Memory.writeByteArray(this.wsa_buffer_address.add(input_len),null_array);
				}else{
					this.wsa_buffer_structure.writeU32(buf_length);
					//this.wsa_buffer_structure = this.wsa_buffer_structure.xor(buf_length);
					//this.wsa_buffer_structure = this.wsa_buffer_structure.add(input_len);
				}
			}
			console.log("================================= SCRIPT END" + threadId);
			send("[END] [THREAD_ID]"+threadId+" [PID]"+Process.id+" [FUNC_NAME]"+hook_function_name);			
		}
	});
}
