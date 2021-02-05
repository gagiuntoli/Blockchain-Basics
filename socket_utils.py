import socket
import pickle

BUFFER_SIZE = 1024

def recvObj(socket):
	new_socket, addr = socket.accept()
	data = b''
	while True:
		d = new_socket.recv(BUFFER_SIZE)
		if not d:
			 break
		data += d
	return pickle.loads(data)

def sendObj(obj, socket):
	data = pickle.dumps(obj)
	socket.send(data)
