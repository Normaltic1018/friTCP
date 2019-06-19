#parsing TEST PY
data = """[HEXDUMP]17 2144cef0  5b 74 65 73 74 31 5d 20 31 32 33
 31 32 33 0d 0a  [test1] 123123..\n2144cf00  00 00 00 00 00 00 00 00 00 00 00 00
 00 00 00 00  ................\n2144cf10  00 00 00 00 00 00 00 00 00 00 00 00 00
 00 00 00  ................\n2144cf20  00 00 00 00 00 00 00 00 00 00 00 00 00 00
 00 00  ................
"""

data_list = data.split("[HEXDUMP]")[1].split()
print(data_list)
start_address = int(data_list[1],16)
a = data_list[1]
b = (int(a,16)) + 16
print(hex(b))
i = 1
indexing = start_address + (i*16)

print(format(indexing,'x'))

hex_list = []
#0~8
for i in range(int(data_list[0])):
	indexing = format(start_address + (int(i/16)*16),'x')
	
	start_index = data_list.index(indexing)
	print("{} : {}".format(start_index,(i%16)))
	hex_list.append(data_list[start_index+1+(i%16)])

print(hex_list)

"""
for i in range(4):
	indexing = format(start_address + (i*16),'x')
	start_index = data_list.index(indexing)

	for hex_byte in data_list[start_index+1:start_index+1+16]:
		hex_list.append(hex_byte)


print(hex_list)
print(len(hex_list))


data_list = data.split()


hex_list = []

for i in range(4):
	indexing = "000000"+str(i)+"0"
	start_index = data_list.index("000000"+str(i)+"0")

	for hex_byte in data_list[start_index+1:start_index+1+16]:
		hex_list.append(hex_byte)


print(hex_list)

"""