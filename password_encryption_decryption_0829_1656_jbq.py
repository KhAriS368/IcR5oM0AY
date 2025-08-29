# 代码生成时间: 2025-08-29 16:56:01
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Password Encryption Decryption Tool using FALCON Framework in Python.
This script provides functions to encrypt and decrypt passwords using AES encryption.
"""

import falcon
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64

# Define a class to handle password encryption and decryption
class PasswordHandler:
    """A class to handle password encryption and decryption using AES."""

    def __init__(self, password, salt, key_length=32, iterations=100000):
        # Initialize the password handler with a password, salt, and key length
        self.password = password
        self.salt = salt
        self.key_length = key_length
        self.iterations = iterations
        self.key = None
        self.iv = None

    def generate_key_and_iv(self):
        # Generate a key and IV using PBKDF2 HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=self.salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        self.key = kdf.derive(self.password.encode())
        self.iv = os.urandom(16)

    def encrypt(self, plaintext):
        # Encrypt the plaintext using AES in CBC mode
        if not self.key or not self.iv:
            self.generate_key_and_iv()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted_data + self.iv)

    def decrypt(self, ciphertext):
        # Decrypt the ciphertext using AES in CBC mode
        if not self.key or not self.iv:
            self.generate_key_and_iv()

        decrypted_iv = base64.b64decode(ciphertext)[16:32]
        if decrypted_iv != self.iv:
            raise ValueError("Invalid IV or wrong password.")

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(decrypted_iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(base64.b64decode(ciphertext)[32:]) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext.decode()

# Define a Falcon API resource to handle encryption and decryption requests
class PasswordResource:
    """A Falcon API resource to handle password encryption and decryption requests."""

    def on_post(self, req, resp):
        # Handle POST requests to encrypt a password
        try:
            password = req.media.get("password")
            salt = os.urandom(16)
            handler = PasswordHandler(password, salt)
            encrypted_password = handler.encrypt(password)
            resp.media = {"encrypted_password": encrypted_password.decode()}
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_500

    def on_put(self, req, resp):
        # Handle PUT requests to decrypt a password
        try:
            password = req.media.get("password")
            salt = base64.b64decode(req.media.get("salt"))
            handler = PasswordHandler(password, salt)
            decrypted_password = handler.decrypt(req.media.get("ciphertext"))
            resp.media = {"decrypted_password": decrypted_password}
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_500

# Create a Falcon API application and add the password resource
app = falcon.App()
app.add_route("/encrypt", PasswordResource())
app.add_route("/decrypt", PasswordResource())