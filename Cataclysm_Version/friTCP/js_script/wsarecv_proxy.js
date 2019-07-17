//Frida Script
var module_list = Process.enumerateModules();
var hook_diction = {};
var input_func_name = "wsarecv";

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

for(var key in hook_diction){
	var hook_module_name = key;
	var hook_function_name = hook_diction[key];
	
	var hookPtr = Module.findExportByName(hook_module_name, hook_function_name);
	//send("[HOOK_INFO][PID]"+Process.id+" [MODULE]"+hook_module_name+" [FUNCTION]"+hook_function_name+" [ADDRESS]"+ hookPtr.toString());
	
	var buf_ptr;
	
	Interceptor.attach(hookPtr,{
		onEnter: function(args){
			this.sock = args[0];
			this.buf = args[1];
			this.buf_len = args[2];
		},
		onLeave: function(retVal){
			
			var op = recv('input',function(value){
				user_write_data = value.payload;
			});
			
			// i is arg index
			var user_write_data;
			
			// IP, PORT Information
			var socket_fd = this.sock.toInt32();
			var socket_address = Socket.peerAddress(socket_fd);
			
			// Buffer Information
			var buf_address = ptr(this.buf);
			var buf_length = retVal.toInt32();

			// if buf_length is so large, it becomes very slow as it stop...
			if(buf_length > 4096){buf_length = 4096;}

			var res = hexdump(buf_address,{offset:0,length:buf_length,header:false,ansi:false});
			
			send("[PROXY]"+"[PID]"+Process.id+" [FUNC_NAME]"+hook_function_name+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res);
		
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
				Memory.writeByteArray(this.buf,input_array);
				input_len = input_array.length;
					
				// fill zero if input_length is longer than origin length
				if(input_len < retVal.toInt32()){
					var null_array = new Array();
					for(var i = 0; i<(this.buf.toInt32()-input_len); i++){null_array[i] = 0;}
						
					Memory.writeByteArray(this.buf.add(input_len),null_array);
				}else{
					this.buf_len = this.buf_len.xor(this.buf_len.toInt32());
					this.buf_len = this.buf_len.add(input_len);
				}
			}	
		}
	});
}
