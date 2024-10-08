#!/usr/bin/env python3

import socket
import sys


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
MSG = " ".join(sys.argv[1:]) #command line input for argument not including the reference file

# operator = sys.argv[0]
# operand = sys.argv[1:]

print("client starting - connecting to server at IP", HOST, "and port", PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"connection established, sending message '{MSG}'")
    s.sendall(bytes(MSG, "utf-8")) #sends command line input to server
    print("message sent, waiting for reply")
    data = s.recv(1024)

print(f"Received response: '{data.decode('utf-8')!r}' [{len(data)} bytes]") #decodes message (but seems unncessary)
print("client is done!")
