from Crypto.PublicKey import RSA
key_pair = RSA.generate(2048)
public_key = key_pair.publickey()
print(public_key.exportKey())
print(key_pair.exportKey())