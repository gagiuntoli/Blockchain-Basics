
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

def generate_keys():

	private = rsa.generate_private_key(
			public_exponent=65537,
			key_size=2048,
			backend=default_backend()
			)

	public = private.public_key()

	public_serialized = public.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
		)
	return private, public_serialized


def sign(message, private_key):

	message = bytes(str(message), 'utf-8')
	signature = private_key.sign(
		message,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH
			),
		 hashes.SHA256()
	)
	return signature


def verify(message, signature, public_serialized):

	public = serialization.load_pem_public_key(
		public_serialized,
		backend=default_backend()
        )
	message = bytes(str(message), 'utf-8')
	try:
		public.verify(
     			signature,
     			message,
     			padding.PSS(
         			mgf=padding.MGF1(hashes.SHA256()),
         			salt_length=padding.PSS.MAX_LENGTH
     			),
     			hashes.SHA256()
 		)
		return True

	except InvalidSignature:
		return False

if __name__ == '__main__':
	pr, pu = generate_keys()
	message = "This is a secret message"
	signature = sign(message, pr)
	correct = verify(message, signature, pu)
	
	if correct:
		print("Success! Good signature")
	else:
		print("Error! Signature is bad")

	# Attack signing with other private key
	pr2, pu2 = generate_keys()
	sig2 = sign(message, pr2)
	correct = verify(message, sig2, pu)
	if correct:
		print("Error! Bad signature checks out!")
	else:
		print("Success! Bad signature detected")

	# Attack changing the message
	message2 = message + "Q"
	correct = verify(message2, sig2, pu)
	if correct:
		print("Error! Tempered message checks out!")
	else:
		print("Success! Tampering detected")
