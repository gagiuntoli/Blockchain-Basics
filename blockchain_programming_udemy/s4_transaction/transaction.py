import sys
sys.path.append("../s2_signature/")
import signature

class Tx:

	inputs = None
	outputs = None
	signatures = None
	reqd = None

	def __init__(self):
		self.inputs = []
		self.outputs = []
		self.signatures = []
		self.reqd = []

	def add_input(self, from_address, amount):
		self.inputs.append((from_address, amount))

	def add_output(self, to_address, amount):
		self.outputs.append((to_address, amount))

	def add_reqd(self, address):
		self.reqd.append(address)

	def sign(self, private):
		message = self.__gather()
		newsig = signature.sign(message, private)
		self.signatures.append(newsig)

	def is_valid(self):

		message = self.__gather()

		total_input = 0
		for address, amount in self.inputs:
			if amount < 0:
				return False
			found = False
			for s in self.signatures:
				if signature.verify(message, s, address):
					found = True
			if not found:
				return False
			total_input += amount

		for address in self.reqd:
			found = False
			for s in self.signatures:
				if signature.verify(message, s, address):
					found = True
			if not found:
				return False

		total_output = 0
		for address, amount in self.outputs:
			if amount < 0:
				return False
			total_output += amount

		if total_output > total_input:
			return False

		return True

	def __gather(self):
		data = []
		data.append(self.inputs)
		data.append(self.outputs)
		data.append(self.reqd)
		return data
	
	def __repr__(self):
		representation = "INPUTS:\n"
		for address, amount in self.inputs:
			representation += str(amount) + " from " + str(address) + "\n"
		representation += "OUTPUTS:\n"
		for address, amount in self.outputs:
			representation += str(amount) + " to " + str(address) + "\n"
		representation += "REQD:\n"
		for address in self.reqd:
			representation += str(address) + "\n"

		representation += "SIGS:\n"
		for s in self.signatures:
			representation += str(s) + "\n"

		representation += "END:\n"
		return representation

if __name__ == "__main__":

	pr1, pu1 = signature.generate_keys()
	pr2, pu2 = signature.generate_keys()
	pr3, pu3 = signature.generate_keys()
	pr4, pu4 = signature.generate_keys()
	
	Tx1 = Tx()
	Tx1.add_input(pu1, 1)
	Tx1.add_output(pu2, 1)
	Tx1.sign(pr1)

	Tx2 = Tx()
	Tx2.add_input(pu1, 2)
	Tx2.add_output(pu2, 1)
	Tx2.add_output(pu3, 1)
	Tx2.sign(pr1)

	Tx3 = Tx()
	Tx3.add_input(pu3, 1.2)
	Tx3.add_output(pu1, 1.1)
	Tx3.add_reqd(pu4)
	Tx3.sign(pr3)
	Tx3.sign(pr4)

	for t in [Tx1, Tx2, Tx3]:
		if t.is_valid():
			print("Success! Tx is valid")
		else:
			print("Error! Tx is invalid")

	# Wrong signatures
	Tx4 = Tx()
	Tx4.add_input(pu1, 1)
	Tx4.add_output(pu2, 1)
	Tx4.sign(pr2)

	# Escrow Tx not signed by the arbiter
	Tx5 = Tx()
	Tx5.add_input(pu3, 1.2)
	Tx5.add_output(pu1, 1.1)
	Tx5.add_reqd(pu4)
	Tx5.sign(pr3)

	# Two input addresses, signed by one
	Tx6 = Tx()
	Tx6.add_input(pu3, 1)
	Tx6.add_input(pu4, 0.1)
	Tx6.add_output(pu1, 1.1)
	Tx6.sign(pr3)
	
	# Output exceed inputs
	Tx7 = Tx()
	Tx7.add_input(pu4, 1.2)
	Tx7.add_output(pu1, 1)
	Tx7.add_output(pu2, 2)
	Tx7.sign(pr4)

	# Negative values
	Tx8 = Tx()
	Tx8.add_input(pu2, -1)
	Tx8.add_output(pu1, -1)
	Tx8.sign(pr2)

	# Modified Tx
	Tx9 = Tx()
	Tx9.add_input(pu2, 1)
	Tx9.add_output(pu1, 1)
	Tx9.sign(pr2)
	Tx9.outputs[0] = (pu3, 1)

	for t in [Tx4, Tx5, Tx6, Tx7, Tx8, Tx9]:
		if t.is_valid():
			print("Error! Bad Tx is valid")
		else:
			print("Success! Bad Tx is invalid")

