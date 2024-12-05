#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64

from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from server.config import Config


class RSACipher():
    """
    RSA encryption, decryption, signature, and verification tools
    """

    def encrypt(self, key, raw):
        """
        Encryption method
        :param key: Public key
        :param raw: Plaintext to be encrypted bytes
        :return: base64 encoded ciphertext bytes
        """
        public_key = RSA.importKey(base64.b64decode(key))
        cipher = Cipher_PKCS1_v1_5.new(public_key)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, key, enc):
        """
        Decryption method
        :param key: Private key
        :param enc: base64 encoded ciphertext bytes
        :return: Decrypted plaintext bytes
        """
        private_key = RSA.importKey(base64.b64decode(key))
        cipher = Cipher_PKCS1_v1_5.new(private_key)
        return cipher.decrypt(base64.b64decode(enc), None)

    def sign(self, key, text):
        """
        Signature method
        :param key: Private key
        :param text: Signed text bytes
        :return: Base64 encoded signature information bytes
        """
        private_key = RSA.importKey(base64.b64decode(key))
        hash_value = SHA256.new(text)
        signer = PKCS1_v1_5.new(private_key)
        signature = signer.sign(hash_value)
        return base64.b64encode(signature)

    def verify(self, key, text, signature):
        """
        Verification method
        :param key: Public key
        :param text: Text to be verified bytes
        :param signature: Base64 encoded signature information bytes
        :return: Verification result bool
        """
        public_key = RSA.importKey(base64.b64decode(key))
        hash_value = SHA256.new(text)
        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(hash_value, base64.b64decode(signature))

if __name__ == '__main__':
    # Client code
    text = b'hello server!'
    cipher = RSACipher()
    # Use server public key encryption
    encrypt_text = cipher.encrypt(Config.SERVER_PUBLIC_KEY, text)
    print('encrypt_text:\n%s' % encrypt_text)
    # Sign with client private key
    signature = cipher.sign(Config.CLIENT_PRIVATE_KEY, encrypt_text)
    print('signature:\n%s' % signature)

    # Server code
    # Use client public key to verify signature
    result = cipher.verify(Config.CLIENT_PUBLIC_KEY, encrypt_text, signature)
    print('result:\n%s' % result)
    # Decrypt with server private key
    decrypt_text = cipher.decrypt(Config.SERVER_PRIVATE_KEY, encrypt_text)
    print('decrypt_text:\n%s' % decrypt_text)

