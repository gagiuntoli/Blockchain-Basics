import socket_utils
from transaction import Tx
from txblock import TxBlock
import signature

wallets = ['localhost']
tx_list = []
head_blocks = [None]

def findLongestBlockchain():
	longest = -1
	long_head = None
	for b in head_blocks:
		current = b
		this_len = 0
		while current != None:
			this_len += 1
			current = current.previous_block
		if this_len > longest:
			long_head = b
			longest = this_len
	return long_head

def minerServer(my_ip, wallet_list, miner_public):
	
	# Open Server connection
	server = socket_utils.newServerConnection('localhost')
	print("connection established")
	# Recv 2 transactions
	for i in range(10):
		newTx = socket_utils.recvObj(server)
		print("Object received: ", i)
		if isinstance(newTx, Tx):
			tx_list.append(newTx)
		if len(tx_list) >= 2:
			break

	# Add Txs to new Block
	newBlock = TxBlock(findLongestBlockchain())
	newBlock.addTx(tx_list[0])
	newBlock.addTx(tx_list[1])

	# compute and add mining reward
	total_in, total_out = newBlock.count_totals()
	mine_reward = Tx()
	mine_reward.add_output(miner_public, 25.0 + total_in - total_out)
	newBlock.addTx(mine_reward)
	print("Reward obtained: ", mine_reward)

	# Find the nonce
	for i in range(10):
		print("Finding nonce")
		newBlock.find_nonce()
		if newBlock.good_nonce():
			print("Good nonce found")
			break
	if not newBlock.good_nonce():
		print("Error: couldn't find nonce")
		return False

	# Send the block to the wallets
	for ip_address in wallets:
		print("Send object: ", ip_address)
		socket_utils.sendObj('localhost', newBlock, 5006)
	head_blocks.remove(newBlock.previous_block)
	head_blocks.append(newBlock)
	return False

my_pr, my_pu = signature.generate_keys()
minerServer('localhost', wallets, my_pu)
