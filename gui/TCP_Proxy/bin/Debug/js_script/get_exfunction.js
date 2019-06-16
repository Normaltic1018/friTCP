//Frida Script
var module_name = '%s';
var select_module = Process.getModuleByName(module_name);
   
var symbol_list = select_module.enumerateExports();
   
for(var idx in symbol_list){
	send(symbol_list[idx].name);
}   
send("");