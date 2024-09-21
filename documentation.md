# Documentation for Simple RPC Client-Server App

## Overview of Application
This project implements a client-server application using the Python package, socket, to perform basic arthimetic functions, addition and subtraction. The server is first initiated (a message is sent to notify listening) and sends a message once the connection has been established. A connection is established when the user initiates the client and inputs an arithmetic argument. This is illustrated in the command-line trace section, which also provides an example output. Subtraction and addition is computed in subsequential order. Output should produce arithmetic computation based on the arguments and the order in which you provide the arguments. This is a very straight forward client-server application with RPC operations.

## Client-Server Message Format
Message format: 
```
MSG = " ".join(sys.argv[1:]) 
print("client starting - connecting to server at IP", HOST, "and port", PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"connection established, sending message '{MSG}'")
    s.sendall(bytes(MSG, "utf-8")) #sends command line input to server
    print("message sent, waiting for reply")
    data = s.recv(1024)
```
* Takes in input from command line to communicate and send to server 
* Client input is represented as MSG
* Tells user that the client is listening and then once connected to server sends another message.

## Server-Client Message Format
Message format:
```
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
```
* Depending on the first argument in the command line, the server either subtracts or adds ('respond' function separates 'verb' aka operator and 'noun(s)' aka operands from command line input).
* After the client communicates argument to server, server performs computation based on addition and subtraction functions. 
* Once the server computes the value based on the argument, it sends the value back to the client and ends the connection between the client and server.

## Command-line Trace & Example Output

First, enable the server in the command line.

```
$ python echo-server.py
server starting - listening for connections at IP 127.0.0.1 and port 65432
connection established with ('127.0.0.1', 53740)
received client message: 'subtract:5:2' [7 bytes]
requested operation is subtraction
request includes 2 arguments: 5 2
result of operation: 3
sending resulting message '5-2=3' back to client
```

Next, input your argument after enabling the client.
```
$ python echo-client.py add 4 5
client starting - connecting to server at IP 127.0.0.1 and port 65432
connection established, sending message 'add 4 5'
message sent, waiting for reply
Received response: '"Received client message: +4:5 [7 bytes]. Requested operation is addition. Request includes 2 arguments: 4 5. Result of operation: 9. Sending resulting message '4+5 = 9' back to client"' [183 bytes]
client is done!
```

## Acknowledgements
https://realpython.com/python-sockets/
https://www.youtube.com/watch?v=3QiPPX-KeSc
https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
https://www.w3schools.com/python/ref_string_lower.asp
https://www.geeksforgeeks.org/check-multiple-conditions-in-if-statement-python/
https://www.w3schools.com/python/python_try_except.asp
https://dbader.org/blog/how-to-make-command-line-commands-with-python
