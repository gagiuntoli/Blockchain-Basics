from transaction import Tx 
import signature
import socket
import socket_utils

TCP_PORT = 5005

if __name__ == "__main__":

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', 1234))
	print("client: connected to server")

	pr1, pu1 = signature.generate_keys()
	pr2, pu2 = signature.generate_keys()
	pr3, pu3 = signature.generate_keys()

	Tx1 = Tx()
	Tx1.add_input(pu1, 2.3)
	Tx1.add_output(pu2, 1.0)
	Tx1.add_output(pu3, 1.1)
	Tx1.sign(pr1)
	print("client: transaction validity =", Tx1.is_valid())

	socket_utils.sendObj(Tx1, s)
	print("client: data sent")
	s.close()

