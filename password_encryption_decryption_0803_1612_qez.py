# 代码生成时间: 2025-08-03 16:12:49
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Password Encryption and Decryption Tool using FALCON framework
"""

from falcon import API, HTTP_400, HTTP_404
import falcon
import base64
from cryptography.fernet import Fernet


# Define the encryption key
# WARNING: In real-world applications, the key should be securely stored and handled.
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)


class PasswordTools:
    """
    A class to handle password encryption and decryption.
    """

    def encrypt(self, plaintext):
        """
        Encrypts a plaintext password.
        
        Args:
        plaintext (str): The password to encrypt.
        
        Returns:
        str: The encrypted password.
        
        Raises:
        ValueError: If the input is not a string.
        """
        if not isinstance(plaintext, str):
            raise ValueError('Input must be a string.')
        
        try:
            encrypted_text = cipher_suite.encrypt(plaintext.encode())
            return encrypted_text.decode()
        except Exception as e:
            raise e

    def decrypt(self, encrypted_text):
        """
        Decrypts an encrypted password.
        
        Args:
        encrypted_text (str): The encrypted password to decrypt.
        
        Returns:
        str: The decrypted password.
        
        Raises:
        ValueError: If the input is not a string.
        """
        if not isinstance(encrypted_text, str):
            raise ValueError('Input must be a string.')
        
        try:
            decrypted_text = cipher_suite.decrypt(encrypted_text.encode())
            return decrypted_text.decode()
        except Exception as e:
            raise e


class PasswordResource:
    """
    A Falcon resource for handling password encryption and decryption.
    """
    def on_post(self, req, resp):
        """
        Handles POST requests for password encryption and decryption.
        
        The request body should contain a JSON object with 'action' and 'password' fields.
        'action' can be either 'encrypt' or 'decrypt'.
        'password' is the password to encrypt or decrypt.
        
        Args:
        req: The Falcon request object.
        resp: The Falcon response object.
        """
        try:
            data = req.media.get('password')
            action = req.media.get('action')
            if action not in ['encrypt', 'decrypt']:
                raise ValueError('Invalid action specified.')
                
            password_tools = PasswordTools()
            if action == 'encrypt':
                encrypted_password = password_tools.encrypt(data)
                resp.media = {'encrypted_password': encrypted_password}
            elif action == 'decrypt':
                decrypted_password = password_tools.decrypt(data)
                resp.media = {'decrypted_password': decrypted_password}
        except KeyError as e:
            raise falcon.HTTPBadRequest('Missing required field.', e)
        except ValueError as e:
            raise falcon.HTTPBadRequest('Invalid input.', e)
        except Exception as e:
            raise falcon.HTTPInternalServerError('An error occurred.', e)


# Initialize the API
api = API()

# Add the resource to the API
api.add_route('/password', PasswordResource())

# Run the API
if __name__ == '__main__':
    import socket
    from wsgiref.simple_server import make_server

    # Allow the server to bind to an already in-use socket
    socket.setdefaulttimeout(1)
    with make_server('localhost', 8000, api) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()