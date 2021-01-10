
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class someClass:
	string = None
	num = 328965
	def __init__(self, mystring):
		self.string = mystring
	def __repr__(self):
		return self.string + "^^^" + str(self.num)

class CBlock:
	data = None
	previous_hash = None
	previous_block = None
	def __init__(self, data, previous_block):
		self.data = data
		self.previous_block = previous_block
		if previous_block != None:
			self.previous_hash = previous_block.computeHash()
	def computeHash(self):
		digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
		digest.update(bytes(str(self.data), 'utf8'))
		digest.update(bytes(str(self.previous_hash), 'utf8'))
		return digest.finalize()


if __name__ == '__main__':

	root = CBlock('I am the root', None)
	B1 = CBlock('I am a Child', root)
	B2 = CBlock('I am B1s brother', root)
	B3 = CBlock(12354, B1)
	B4 = CBlock(someClass("Hi there!"), B3)
	B5 = CBlock("Top block", B4)

	# root -> B1 -> B3 -> B4 -> B5
	#      \> B2

	for b in [B1, B2, B3, B4, B5]:
		if b.previous_block.computeHash() == b.previous_hash:
			print ("Success! Hash is good")
		else:
			print ("Error! Hash is not good")

	B3.data = 12345
	if B4.previous_block.computeHash() == B4.previous_hash:
		print ("Error! Couldn't detect tampering")
	else:
		print ("Success! Tampering detected")

	B4.data.num = 666666
	if B5.previous_block.computeHash() == B5.previous_hash:
		print ("Error! Couldn't detect tampering")
	else:
		print ("Success! Tampering detected")

