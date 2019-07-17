//Frida Script
var module_list = Process.enumerateModules();
var hook_diction = {};
var input_func_name = "wsasend";

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
			var op = recv('input',function(value){
				//console.log("GET POST DATA");
				user_write_data = value.payload;
			});
			
			var buf_index;
			buf_index = 1;
			
			// i is arg index
			var user_write_data;
			
			// IP, PORT Information
			var socket_fd = args[0].toInt32();
			var socket_address = Socket.peerAddress(socket_fd);
			
			// Buffer Information
			var buf_address = ptr(args[buf_index]);
			var buf_length = args[buf_index+1].toInt32();

			// if buf_length is so large, it becomes very slow as it stop...
			if(buf_length > 4096){buf_length = 4096;}

			var res = hexdump(buf_address,{offset:0,length:buf_length,header:false,ansi:false});
			
			send("[PROXY]"+"[PID]"+Process.id+" [FUNC_NAME]"+hook_function_name+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res);
		
			//send("[INTERCEPT]");
			//console.log("wait start");
			// Receive User Data
			op.wait();
			//user_write_data = "";
			
			//console.log("wait end");
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
				Memory.writeByteArray(args[buf_index],input_array);
				input_len = input_array.length;
					
				// fill zero if input_length is longer than origin length
				if(input_len < args[buf_index+1].toInt32()){
					var null_array = new Array();
					for(var i = 0; i<(args[buf_index+1].toInt32()-input_len); i++){null_array[i] = 0;}
						
					Memory.writeByteArray(args[buf_index].add(input_len),null_array);
				}else{
					args[buf_index+1] = args[buf_index+1].xor(args[buf_index+1].toInt32());
					args[buf_index+1] = args[buf_index+1].add(input_len);
					buf_ptr = args[buf_index];
				}
			}
		}
	});
}
