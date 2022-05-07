EOT = chr(4)   # End-of-Transmission character

class ConfirmationError(Exception):
    pass

'''
ConnectionFeedbackLoop:-

I have created this feedback system on top of socket module.
It is created because there is no guarantee in socket that 
data sent from one sendall() will be received by only one corresponding
recv(). Sometimes data from multiple sendall() is received by
a single recv() and sometimes it will take multiple recv() calls to 
get complete data from one sendall().

This class completely solves that problem. A single sendall() of
this class will always be recieved by a single recv() call and multiple
sendall() cannot be received by one recv().

This is done by appending a 'End-of-Transmission' character at the end
each time data is sent. Also after recv() gets the complete data, it 
sends a EOT character back to sender as a confirmation for successful
data transfer.

Attributes:-
connection - Pass a socket connection here.

Methods:-
sendall(data) - send bytes-like object 'data'
recv(buffer_size) - receive data
'''
class ConnectionFeedbackLoop:
    def __init__(self, connection):
        self.c = connection
        
    def sendall(self, data: bytes):
        self.c.sendall(data)
        self.c.sendall(EOT.encode())
        if self.c.recv(1).decode() != EOT:
            raise ConfirmationError('No receiving conformation')
        
    def recv(self, buffer_size: int):
        b = bytearray(self.c.recv(buffer_size))
        if len(b) == 0:
            return b''
        
        while b[-1] != ord(EOT):
            b += bytearray(self.c.recv(buffer_size))
        self.c.sendall(EOT.encode())
        return bytes(b[:-1])