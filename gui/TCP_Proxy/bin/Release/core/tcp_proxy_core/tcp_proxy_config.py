import os

version = 0.3

js_path = os.path.dirname(os.path.abspath(__file__)) + "\\..\\js_script\\"

commands = {"proxy":"capture the api in capture_list",
"set":"Set Options",
"exit":"Exit This Script"}

settings_validation = {"mode":["hex", "string"],
"capture_list":["send","recv","wsasend","wsarecv","recvfrom","wsarecvfrom"],
"intercept":["on","off"]
}

settings = {"mode":"hex",
"capture_list":["send"],
"intercept":"off"
}
