
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

digest = hashes.Hash(hashes.SHA256(), backend=default_backend())

digest.update(b"abc")
digest.update(b"123")
hash1 = digest.finalize()

print(hash1)

digest = hashes.Hash(hashes.SHA256(), backend=default_backend())

digest.update(b"abc")
digest.update(b"124")
hash2 = digest.finalize()

print(hash2)
