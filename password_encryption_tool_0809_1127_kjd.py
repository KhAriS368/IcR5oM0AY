# 代码生成时间: 2025-08-09 11:27:22
#!/usr/bin/env python
"""
Password Encryption Tool using Falcon framework
This tool provides password encryption and decryption features.

@author: yourname
@version: 1.0
"""

import falcon
import hashlib
import base64

# Define a class for handling password encryption and decryption
class PasswordHandler:
    def __init__(self):
        pass

    def encrypt_password(self, password):
        """
        Encrypts the given password using SHA-256 hashing and base64 encoding.

        Args:
            password (str): The password to be encrypted.

        Returns:
            str: The encrypted password.

        Raises:
            ValueError: If the input password is not a string.
        """
        if not isinstance(password, str):
            raise ValueError("Password must be a string.")

        # Create a SHA-256 hash of the password
        sha256_hash = hashlib.sha256(password.encode())

        # Get the digest of the hash and encode it in base64
        encrypted_password = base64.b64encode(sha256_hash.digest()).decode()

        return encrypted_password

    def decrypt_password(self, encrypted_password):
        """
        Decrypts the given encrypted password using base64 decoding and SHA-256 hashing.

        Args:
            encrypted_password (str): The encrypted password to be decrypted.

        Returns:
            str: The decrypted password.

        Raises:
            ValueError: If the input encrypted password is not a string.
            ValueError: If the decryption fails.
        """
        if not isinstance(encrypted_password, str):
            raise ValueError("Encrypted password must be a string.")

        try:
            # Decode the base64 encoded encrypted password
            decoded_encrypted_password = base64.b64decode(encrypted_password)

            # Create a SHA-256 hash of the decoded encrypted password
            sha256_hash = hashlib.sha256(decoded_encrypted_password)

            # Get the digest of the hash
            digest = sha256_hash.digest()

            # Convert the digest back to a string
            password = digest.decode()

            return password

        except Exception as e:
            raise ValueError("Decryption failed: " + str(e))

# Define a Falcon API resource for handling requests
class PasswordResource:
    def __init__(self):
        self.password_handler = PasswordHandler()

    def on_get(self, req, resp):
        # Handle GET requests to encrypt a password
        if 'password' in req.params:
            try:
                password = req.params['password']
                encrypted_password = self.password_handler.encrypt_password(password)
                resp.status = falcon.HTTP_OK
                resp.media = {'encrypted_password': encrypted_password}
            except ValueError as e:
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.media = {'error': str(e)}
        else:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.media = {'error': 'Password parameter is missing'}

    def on_post(self, req, resp):
        # Handle POST requests to decrypt a password
        try:
            encrypted_password = req.media['encrypted_password']
            password = self.password_handler.decrypt_password(encrypted_password)
            resp.status = falcon.HTTP_OK
            resp.media = {'password': password}
        except ValueError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.media = {'error': str(e)}

# Create a Falcon app instance
app = falcon.App()

# Add the PasswordResource to the app
app.add_route('/password', PasswordResource())