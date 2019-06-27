//Frida Script
var module_list = Process.enumerateModules();
      
for(var idx in module_list){
	send(module_list[idx].name);
}   
send("");