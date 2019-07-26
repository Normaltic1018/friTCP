//Frida Script
var module_list = Process.enumerateModules();
var hook_diction = {};
var input_func_name = "wsasend";
/*
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
*/
var hook_module_name = "Secur32.dll";
var hook_function_name = "DecryptMessage"
	
var hookPtr = Module.findExportByName(hook_module_name, hook_function_name);
//send("[HOOK_INFO][PID]"+Process.id+" [MODULE]"+hook_module_name+" [FUNCTION]"+hook_function_name+" [ADDRESS]"+ hookPtr.toString());
	
var buf_ptr;
var call_num = 0;

Interceptor.attach(hookPtr,{
	onEnter: function(args){
		// wait for ready gui
		if(call_num > 5000){
			call_num = 0;
		}else{
			call_num = call_num + 1;
		}
		var buf_index;
		buf_index = 1;
		
		this.pMessage_address = ptr(args[buf_index]);
		var threadId = Process.getCurrentThreadId();
		console.log("================================= SCRIPT START" + threadId+"_"+call_num);
		send("[KNOCK] [THREAD_ID]"+threadId+"_"+call_num+" [PID]"+Process.id+" [FUNC_NAME]"+hook_function_name);
		var gogo = recv(threadId+"_"+call_num,function(value){
			//console.log("GET POST DATA");
			console.log("GOGO Script");
		});
		
		gogo.wait();
	},
	onLeave: function(retVal){
		var threadId = Process.getCurrentThreadId();
		console.log("================================= SCRIPT RESTART" + threadId+"_"+call_num);
		console.log("GOGO START");
		var op = recv('input',function(value){
			//console.log("GET POST DATA");
			user_write_data = value.payload;
		});
					
			// i is arg index
		var user_write_data;
			
		// Buffer Information
		//var pMessage_address = ptr(args[buf_index]);
		//console.log("pMessage_address : " + (pMessage_address));
		
		//console.log(Memory.readByteArray(pMessage_address,64));
		
		var pBuffer_address = Memory.readPointer(this.pMessage_address.add(8));
		var num_of_buffer = Memory.readULong(this.pMessage_address.add(4));
		console.log("pBUffer_address : "+pBuffer_address);
		
		var buf_length;
		var buf_address;
		
		console.log("num of buffer : " + num_of_buffer);
		for(var i=0;i<num_of_buffer;i++){
			var index_of_type = (i * 12) + 4;
			var type_value = Memory.readULong(pBuffer_address.add(index_of_type));
			if(type_value == 1){
				buf_length = Memory.readULong(pBuffer_address.add(index_of_type-4));
				buf_address = Memory.readPointer(pBuffer_address.add(index_of_type+4));
				break;
			}
		}
		console.log(Memory.readByteArray(pBuffer_address,256));
		
		console.log("buf_len : " + buf_length);
		console.log("buf_address : " + buf_address);
		
		//console.log(Memory.readByteArray(buf_address,32));
		// if buf_length is so large, it becomes very slow as it stop...
		//if(buf_length > 4096){buf_length = 4096;}
		
		if((buf_address === undefined || buf_address === null || buf_length === undefined || buf_length ===null) == false){
			var res = hexdump(buf_address,{offset:0,length:buf_length,header:false,ansi:false});
				
			send("[PROXY]"+"[PID]"+Process.id+" [FUNC_NAME]"+hook_function_name+" [IP]- [PORT]- "+"[HEXDUMP]"+buf_length+" " + res);
			
			op.wait();
				
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
				Memory.writeByteArray(buf_address,input_array);
				input_len = input_array.length;
						
				// fill zero if input_length is longer than origin length
				if(input_len < buf_length){
					var null_array = new Array();
					for(var i = 0; i<(buf_length-input_len); i++){null_array[i] = 0;}
							
					Memory.writeByteArray(buf_address.add(input_len),null_array);
				}else{
					pBuffer_address.add(12).replace(input_len);
				}
			}
		}else{
			console.log("UNDEFINED....@@");
			send("[PROXY]"+"[PID]"+Process.id+" [FUNC_NAME]"+hook_function_name+" [IP]- [PORT]- "+"[HEXDUMP]"+0+" " + "");
		}
		console.log("================================= SCRIPT END" + threadId+"_"+call_num);
		send("[END] [THREAD_ID]"+threadId+"_"+call_num+" [PID]"+Process.id+" [FUNC_NAME]"+hook_function_name);
	}
});
	
	
/*
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
*/