import socket_utils
import signature
from transaction import Tx 

head_blocks = [None]

pr1, pu1 = signature.generate_keys()
pr2, pu2 = signature.generate_keys()
pr3, pu3 = signature.generate_keys()

Tx1 = Tx()
Tx2 = Tx()

Tx1.add_input(pu1, 4.0)
Tx1.add_input(pu2, 1.0)
Tx1.add_output(pu3, 4.8)
Tx2.add_input(pu3, 4.0)
Tx2.add_output(pu2, 4.0)
Tx2.add_reqd(pu1)

Tx1.sign(pr1)
Tx1.sign(pr2)
Tx2.sign(pr3)
Tx2.sign(pr1)

try:
	socket_utils.sendObj('localhost', Tx1)
	print("Tx1 sent")
	socket_utils.sendObj('localhost', Tx2)
	print("Tx2 sent")
except:
	print ("Error! Connection unsuccessful")

server = socket_utils.newServerConnection('localhost', 5006)
print("Connection established")
for i in range(10):
	newBlock = socket_utils.recvObj(server)
	print("Object received: ", i)
	if newBlock:
		break
server.close()

if newBlock.is_valid():
	print("Success! Block is valid")
if newBlock.good_nonce():
	print("Success! Nonce is valid")

for tx in newBlock.data:
	try:
		if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
			print("Tx1 is present")
	except:
			print("Tx1 in not here")
	try:
		if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
			print("Tx2 is present")
	except:
			print("Tx2 in not here")

# Add new block to the blockchain
for b in head_blocks:
	if newBlock.previous_hash == b.computeHash():
		newBlock.previous_block = b
		head_blocks.remove(b)
		head_blocks.append(newBlock)

