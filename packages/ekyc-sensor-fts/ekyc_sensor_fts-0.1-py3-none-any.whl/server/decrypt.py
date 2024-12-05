from server.AESCipher import AESCipher
from server.RSACipher import RSACipher
from server.config import Config
rsa_cipher = RSACipher()

def decrypt(file_path):
    with open(file_path) as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
    # Encrypt the aes key using the server public key
    encrypt_key = lines[2]
    text = lines[0]
    aes_key = rsa_cipher.decrypt(Config.SERVER_PRIVATE_KEY, encrypt_key)
    # Use aes private key to decrypt ciphertext
    aes_cipher = AESCipher(aes_key)
    decrypt_text = aes_cipher.decrypt(text)
    # print('decrypt_text:\n%s' % decrypt_text)
    return decrypt_text