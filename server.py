import socket
from base64 import b64decode, b64encode
from tools import ConnectionFeedbackLoop

user = "Chaitanya"

s = socket.create_server(('localhost', 50000))
print('Server running...')

connection, address = s.accept()

transmitter = ConnectionFeedbackLoop(connection)

transmitter.sendall(f'Connected with {user}\nWaiting for a message...'.encode())
print(transmitter.recv(1024).decode())

while True:
    msg = input("-> ")
    
    if msg == "#send":
        while True:
            path = input('Filepath: ')
            if path == '':
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
                
        if path == '':
            continue
        
    elif msg == "":
        msg = " "
    transmitter.sendall(msg.encode())
    
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