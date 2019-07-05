//TCP Proxy AGENT Script
// Shell
while(true){
	var cmd = "";
	send("[AGENT_SHELL]");
	var op = recv('shell',function(value){
		cmd = value.payload;
	});
	op.wait();
	
	if(cmd.startsWith("hook_")){
		//hook command
		var func_name = cmd.substring(5);
		console.log(func_name);
		if(func_name.includes("send")){
			//send
			hook_function("WS2_32.dll","send");
			console.log("send hook");
		}else if(func_name.includes("recv")){
			// recv
			console.log("recv hook");
		}else{
			// else function
		}
	}else if(cmd.startsWith("search_func")){
		//search
	}else if(cmd == "exit"){
		// before exitk, unload script
		break;
	}
}

function test_onEnter(args){
	send("[intercept_on/off]");
	var op = recv('intercept',function(v alue){
		intercept_flag = value.payload;
	});
	op.wait();
			
			//send("["+hook_module_name+":"+hook_function_name+"]"+' Caught');
			var buf_index;
			buf_index = 1;
			
			// i is arg index
			var user_write_data;
			
			var socket_fd = args[0].toInt32();
			
			var socket_address = Socket.peerAddress(socket_fd);
			//send('{"ip":"'+socket_address.ip+'","port":"'+socket_address.port+'"}')
			
			var buf_address = ptr(args[buf_index]);
			//for (key in memory_arg){
				//console.log('key : ' + key + ', value : ' + memory_arg[key]);
			//}
			var buf_length = args[buf_index+1].toInt32();

			// if buf_length is so large, it becomes very slow as it stop...
			if(buf_length > 4096){buf_length = 4096;}

			var res = hexdump(buf_address,{offset:0,length:buf_length,header:false,ansi:false});
			
			//var res = memory_arg.readByteArray(64);
			send("[PROXY][INTERCEPT]"+intercept_flag+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res);
			//send("[HEXDUMP]"+buf_length+" " + res);
	
	this.argu = "test";
	var socket_fd = args[0].toInt32();
	send("Send Enter!");
	send(socket_fd);
}

function test_onLeave(retval){
	send(this.argu);
}

function hook_function(module_name,function_name){
	// hook function
	var hookPtr = Module.findExportByName(module_name, function_name);
	
	Interceptor.attach(hookPtr,{
		onEnter: test_onEnter,
		onLeave: test_onLeave
	});
}
/*
function test_onEnter(args){
	console.log("Send Enter!");
}

function send_hook_onEnter(args){
			
			send("[intercept_on/off]");
			var op = recv('intercept',function(value){
				intercept_flag = value.payload;
			});
			op.wait();
			
			//send("["+hook_module_name+":"+hook_function_name+"]"+' Caught');
			var buf_index;
			buf_index = 1;
			
			// i is arg index
			var user_write_data;
			
			var socket_fd = args[0].toInt32();
			
			var socket_address = Socket.peerAddress(socket_fd);
			//send('{"ip":"'+socket_address.ip+'","port":"'+socket_address.port+'"}')
			
			var buf_address = ptr(args[buf_index]);
			//for (key in memory_arg){
				//console.log('key : ' + key + ', value : ' + memory_arg[key]);
			//}
			var buf_length = args[buf_index+1].toInt32();

			// if buf_length is so large, it becomes very slow as it stop...
			if(buf_length > 4096){buf_length = 4096;}

			var res = hexdump(buf_address,{offset:0,length:buf_length,header:false,ansi:false});
			
			//var res = memory_arg.readByteArray(64);
			send("[PROXY][INTERCEPT]"+intercept_flag+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res);
			//send("[HEXDUMP]"+buf_length+" " + res);


			
			if(intercept_flag == "on"){
				send("interactive");
				var op = recv('input',function(value){
					user_write_data = value.payload;
				});
				op.wait();
				
				// GET MODE
				send("[GET_MODE]");
				op = recv('input',function(value){
					mode = value.payload;
				});
				op.wait();
				
				var input_len;
				input_len = user_write_data.length;
				if(input_len != 0){
					if(mode == "hex"){
						// Hex mode
						user_write_data = user_write_data + " 0d 0a";
						var list_user_data = user_write_data.split(" ");
						var input_array = new Array();
						
						for(var i in list_user_data){
							input_array[i] = parseInt(list_user_data[i],16);
						}
						Memory.writeByteArray(args[buf_index],input_array);
						input_len = input_array.length;
					}else{
						// String mode
						user_write_data = user_write_data + "\n";
					
						input_len = user_write_data.length;
					
						Memory.writeAnsiString(args[buf_index], user_write_data);
					}
										
					if(input_len < args[buf_index+1].toInt32()){
						var null_array = new Array();
						for(var i = 0; i<(args[buf_index+1].toInt32()-input_len); i++){null_array[i] = 0;}
						
						Memory.writeByteArray(args[buf_index].add(input_len),null_array);
					}else{
						args[buf_index+1] = args[buf_index+1].xor(args[buf_index+1].toInt32());
						args[buf_index+1] = args[buf_index+1].add(input_len);
						buf_ptr = args[buf_index];
					}
					//send('Modified buf:');
					//var res = hexdump(buf_address,{offset:0,length:64,header:false,ansi:false});
					//send("[HEXDUMP]" + res);
					//console.log(Memory.readByteArray(args[buf_index],64));
				}
			}
}


send("[intercept_on/off]");
var op = recv('intercept',function(value){
	intercept_flag = value.payload;
});
op.wait();



var module_list = Process.enumerateModules();
var hook_diction = {};
var input_func_name = "%s";
var mode = "%s";
var intercept_flag;
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
	send("[HOOK_INFO][PID]"+Process.id+" [MODULE]"+hook_module_name+" [FUNCTION]"+hook_function_name+" [ADDRESS]"+ hookPtr.toString());
	
	var buf_ptr;
	
	Interceptor.attach(hookPtr,{
		onEnter: function(args){
			
			send("[intercept_on/off]");
			var op = recv('intercept',function(value){
				intercept_flag = value.payload;
			});
			op.wait();
			
			//send("["+hook_module_name+":"+hook_function_name+"]"+' Caught');
			var buf_index;
			buf_index = 1;
			
			// i is arg index
			var user_write_data;
			
			var socket_fd = args[0].toInt32();
			
			var socket_address = Socket.peerAddress(socket_fd);
			//send('{"ip":"'+socket_address.ip+'","port":"'+socket_address.port+'"}')
			
			var buf_address = ptr(args[buf_index]);
			//for (key in memory_arg){
				//console.log('key : ' + key + ', value : ' + memory_arg[key]);
			//}
			var buf_length = args[buf_index+1].toInt32();

			// if buf_length is so large, it becomes very slow as it stop...
			if(buf_length > 4096){buf_length = 4096;}

			var res = hexdump(buf_address,{offset:0,length:buf_length,header:false,ansi:false});
			
			//var res = memory_arg.readByteArray(64);
			send("[PROXY][INTERCEPT]"+intercept_flag+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res);
			//send("[HEXDUMP]"+buf_length+" " + res);


			
			if(intercept_flag == "on"){
				send("interactive");
				var op = recv('input',function(value){
					user_write_data = value.payload;
				});
				op.wait();
				
				// GET MODE
				send("[GET_MODE]");
				op = recv('input',function(value){
					mode = value.payload;
				});
				op.wait();
				
				var input_len;
				input_len = user_write_data.length;
				if(input_len != 0){
					if(mode == "hex"){
						// Hex mode
						user_write_data = user_write_data + " 0d 0a";
						var list_user_data = user_write_data.split(" ");
						var input_array = new Array();
						
						for(var i in list_user_data){
							input_array[i] = parseInt(list_user_data[i],16);
						}
						Memory.writeByteArray(args[buf_index],input_array);
						input_len = input_array.length;
					}else{
						// String mode
						user_write_data = user_write_data + "\n";
					
						input_len = user_write_data.length;
					
						Memory.writeAnsiString(args[buf_index], user_write_data);
					}
										
					if(input_len < args[buf_index+1].toInt32()){
						var null_array = new Array();
						for(var i = 0; i<(args[buf_index+1].toInt32()-input_len); i++){null_array[i] = 0;}
						
						Memory.writeByteArray(args[buf_index].add(input_len),null_array);
					}else{
						args[buf_index+1] = args[buf_index+1].xor(args[buf_index+1].toInt32());
						args[buf_index+1] = args[buf_index+1].add(input_len);
						buf_ptr = args[buf_index];
					}
					//send('Modified buf:');
					//var res = hexdump(buf_address,{offset:0,length:64,header:false,ansi:false});
					//send("[HEXDUMP]" + res);
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
*/