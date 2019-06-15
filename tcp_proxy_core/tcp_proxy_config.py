version = 0.3

commands = {"proxy":"capture the api in capture_list",
"set":"Set Options",
"exit":"Exit This Script"}

settings_validation = {"mode":["hex", "string"],
"capture_list":["send","recv","wsasend","wsarecv","recvfrom","wsarecvfrom"]
}

settings = {"mode":"string",
"capture_list":["send"]
}