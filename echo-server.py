#!/usr/bin/env python3

# pylint: disable=broad-exception-caught
# !/usr/bin/env python3

import socket
import numpy as np

#function to add input values
def add(args):
    add_value = sum(args)
    return add_value

#function to subtract input values
def subtract(args):
    sub_value = args[0]
    for value in args[1:]:
        sub_value -= value
    return sub_value

#determines which computation to perform based on client input
def respond(args):
    try:
        client_input = args.decode('utf-8')
        operator, *operand = client_input.split(' ')
        operand_array = np.array(operand, dtype = int)
        operand_list = list(operand_array)

        if operator.lower() == "add": #performs addition 
            computation = add(operand_list)
            # computation = sum(operand_list)
            output = f"Received client message: +{':'.join(map(str,operand_list))} [{len(args)} bytes]. Requested operation is addition. Request includes {len(operand_list)} arguments: {' '.join(map(str,operand_list))}. Result of operation: {computation}. Sending resulting message '{'+'.join(map(str,operand_list))} = {computation}' back to client"
        if (operator.lower() == "minus" or operator.lower() == "subtract"): #performs subtraction
            computation = subtract(operand_list)
            # computation = operand_list[0] - sum(operand_list[1:])
            output = f"Received client message: -{':'.join(map(str,operand_list))} [{len(args)} bytes]. Requested operation is subtraction. Request includes {len(operand_list)} arguments: {' '.join(map(str,operand_list))}. Result of operation: {computation}. Sending resulting message '{operand_list[0]}-{'-'.join(map(str, operand_list[1:]))} = {computation}' back to client"
        return output
    except Exception as e: #throws error message if user inputs arthimetic function that's not addition or subtraction
        return f"Error Message: Unknown operand or {e}"





        
    # except Exception as e:
    #     error_message = f"Error Message: {str(e)}".encode('utf-8')
    #     return error_message




HOST = "127.0.0.1"  # Standard loopback interface address (localhost) (running and accessed locally)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

print("server starting - listening for connections at IP", HOST, "and port", PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # s becomes destination send to file, socket --> set up server accept inputs at this destination
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            # print(f"Received client message: '{data!r}' [{len(data)} bytes]")


            server_response = respond(data) #process data sent from client
            print(server_response.encode('utf-8')) 
            # print(f"echoing '{data!r}' back to client") #"I'm not home!".encode('utf-8') turns into byte like object
            conn.sendall(server_response.encode('utf-8')) #sends processed data back to client

print("server is done!")
