//Frida Script
var module_list = Process.enumerateModules();
var hook_diction = {};
      
for(var idx in module_list){
	// Find Function
	var select_module = Process.getModuleByName(module_list[idx].name);
   
	var symbol_list = select_module.enumerateExports();
   
	for(var sym_idx in symbol_list){
		// Compare
		if(symbol_list[sym_idx].name == "%s"){
			hook_diction[module_list[idx].name] = symbol_list[sym_idx].name;
		}
	}
}  

for(var key in hook_diction){
	var hook_module_name = key;
	var hook_function_name = hook_diction[key];
	
	var hookPtr = Module.findExportByName(hook_module_name, hook_function_name);
	send("["+hook_module_name+":"+hook_function_name+"]'s "+' address :' + hookPtr.toString());
	
	Interceptor.attach(hookPtr,{
		onEnter: function(args){
			send("["+hook_module_name+":"+hook_function_name+"]"+' Called');
			for(var i=0; i<10;i++){
				try{
					send("\t-arg["+i+"] : "+ args[i] +"( "+ Memory.readCString(args[i]) +" )");
					//console.log(Memory.readByteArray(args[4],64));
				}catch(e){
					send("\t-arg["+i+"] : "+ args[i] +"( "+ args[i].toInt32() +" )");
				}
				// To see hex dump
				//console.log(Memory.readByteArray(args[4],64));
			}
		},
		onLeave: function (retval){
			try{
				send("\t-Return Value : "+ retval +"( "+ Memory.readCString(retval) +" )");
			}catch(e){
				send("\t-Return Value : "+ retval +"( "+ retval.toInt32() +" )");
			}
		}
	});
}
