//Frida Script
var module_list = Process.enumerateModules();
var hook_diction = {};
var input_func_name = "%s";
var mode = "%s";
var intercept_flag ="on";
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
	send("["+hook_module_name+":"+hook_function_name+"]'s "+' address :' + hookPtr.toString());
	
	var buf_ptr;
	
	Interceptor.attach(hookPtr,{
		onEnter: function(args){
			send("["+hook_module_name+":"+hook_function_name+"]"+' Caught');
			var buf_index;
			buf_index = 1;
			
			// i is arg index
			var user_write_data;
			
			var socket_fd = args[0].toInt32();
			
			var socket_address = Socket.peerAddress(socket_fd);
			send('{"ip":"'+socket_address.ip+'","port":"'+socket_address.port+'"}')
			
			var buf_address = ptr(args[buf_index]);
			//for (key in memory_arg){
				//console.log('key : ' + key + ', value : ' + memory_arg[key]);
			//}
			var buf_length = args[buf_index+1].toInt32();
			var res = hexdump(buf_address,{offset:0,length:64,header:false,ansi:false});
			//var res = memory_arg.readByteArray(64);
			send("[HEXDUMP]"+buf_length+" " + res);

			send("[intercept_on/off]");
			var op = recv('intercept',function(value){
				intercept_flag = value.payload;
			});
			op.wait();
			
			if(intercept_flag == "on"){
				send("interactive");
				var op = recv('input',function(value){
					user_write_data = value.payload;
				});
				op.wait();
				var input_len;
				input_len = user_write_data.length;
				if(input_len != 0){
					// If a particular character must end in the end
					user_write_data = user_write_data + "\n";
					
					input_len = user_write_data.length;
					
					Memory.writeAnsiString(args[buf_index], user_write_data);
					if(input_len < args[buf_index+1].toInt32()){
						var null_array = new Array();
						for(var i = 0; i<(args[buf_index+1].toInt32()-input_len); i++){null_array[i] = 0;}
						
						Memory.writeByteArray(args[buf_index].add(input_len),null_array);
					}else{
						args[buf_index+1] = args[buf_index+1].xor(args[buf_index+1].toInt32());
						args[buf_index+1] = args[buf_index+1].add(input_len);
						buf_ptr = args[buf_index];
					}
					send('Modified buf:');
					var res = hexdump(buf_address,{offset:0,length:64,header:false,ansi:false});
					send("[HEXDUMP]" + res);
					//console.log(Memory.readByteArray(args[buf_index],64));
				}
			}
		},
		onLeave: function (retval){
			if(intercept_flag == "on"){
				try{
					send("\t-Return Value : "+ retval +"( "+ Memory.readCString(retval) +" )");
				}catch(e){
					send("\t-Return Value : "+ retval +"( "+ retval.toInt32() +" )");
				}
			}
		}
	});
}
