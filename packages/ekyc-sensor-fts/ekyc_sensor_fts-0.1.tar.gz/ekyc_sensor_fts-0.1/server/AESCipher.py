#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AESCipher:
    """
    AES encryption and decryption toolsx
    """

    def __init__(self, key):
        self.key = key
        # Here directly use key as iv
        self.iv = key

    def encrypt(self, raw):
        """
        Encryption method
        :param raw: Ciphertext to be encrypted str
        :return: base64 encoded ciphertext str
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(self.__pad(raw).encode())).decode()

    def decrypt(self, enc):
        """
        Decryption method
        :param enc: base64 encoded ciphertext str
        :return: Decrypted plaintext str
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.__unpad(cipher.decrypt(base64.b64decode(enc)).decode())

    def __pad(self, text):
        # Filling method, the encrypted content must be a multiple of 16 bytes
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        # __unpad
        pad = ord(text[-1])
        return text[:-pad]


if __name__ == '__main__':
    # Randomly generate 16-bit aes key
    cipher = AESCipher(get_random_bytes(16))
    text = "hello server!"
    encrypt = cipher.encrypt(text)
    print('encrypt:\n%s' % encrypt)
    decrypt = cipher.decrypt(encrypt)
    print('decrypt:\n%s' % decrypt)
