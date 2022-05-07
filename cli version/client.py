import socket
import sys
from base64 import b64decode, b64encode
from tools import ConnectionFeedbackLoop

user = "Anushka"
server = ('2.tcp.ngrok.io', 11633)

connection = socket.create_connection(server)

transmitter = ConnectionFeedbackLoop(connection)

confirmation_msg = transmitter.recv(1024).decode()
if confirmation_msg != "":
    print(confirmation_msg)
else:
    print('Server is not active!')
    sys.exit()

transmitter.sendall(f"Connected with {user}".encode())

while True:
    print('-: ', end = '', flush=True)
    try:
        reply = transmitter.recv(1024).decode()

    except ConnectionAbortedError:
        print('Disconnected!')
        break
    
    if reply == '' or reply.lower() == 'disconnect':
        print('Disconnected!')
        break
        
    elif reply == "#send":
        filename = transmitter.recv(1024).decode()
        file = b64decode(transmitter.recv(10*1024))
        
        with open(filename, 'wb') as f:
            f.write(file)
            print(f'{filename} received!')
            
    else:
        print(reply)
    
    msg = input("-> ")
    
    if msg == "#send":
        while True:
            path = input('Filepath: ')
            if path == '':
                msg = ' '
                break
            try:
                with open(path, 'rb') as f:
                    transmitter.sendall(msg.encode())
                    msg = b64encode(f.read()).decode()
                    transmitter.sendall(path.split('\\')[-1].encode())
                    print("Sending File...")
                    break
            except FileNotFoundError:
                print('File not found')
        
    elif msg == "":
        msg = " "
    transmitter.sendall(msg.encode())