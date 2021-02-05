import txblock
import socket
import socket_utils

if __name__ == "__main__":

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('localhost', 1234))
	s.listen()

	print("server: waiting from data")
	obj = socket_utils.recvObj(s)

	print("server: receiving object", obj.__class__.__name__)
	print("server: money input", obj.inputs[0][1])
	print("server: money output", obj.outputs[0][1])
	print("server: money output", obj.outputs[1][1])
	print("server: transaction validity =", obj.is_valid())
	s.close()
