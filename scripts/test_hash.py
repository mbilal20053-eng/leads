import hashlib
import time

row = ("John Doe", "John", "Doe", "john@example.com", "555-1234", "Acme Corp", "VP Sales")
norm_key = "\t".join(s.strip().lower() for s in row).encode('utf-8')
h = hashlib.blake2b(norm_key, digest_size=8).digest()
print("Hash sample:", h.hex())
