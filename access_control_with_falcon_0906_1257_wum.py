# 代码生成时间: 2025-09-06 12:57:51
#!/usr/bin/env python

"""
A Falcon application that demonstrates access control.
"""

from falcon import API, Request, Response
from falcon.auth import BasicAuth
from falcon_auth import FalconBasicAuthMiddleware
from falcon_auth.backends import SimpleAuthBackend
import hashlib

# Simple authentication backend
class BasicAuthBackend(SimpleAuthBackend):
    def __init__(self):
        self._users = {
            'admin': hashlib.sha256('admin_password'.encode()).hexdigest()  # Hashed password
        }

    def authenticate(self, username, password):
        if username in self._users:
            password_sha256 = hashlib.sha256(password.encode()).hexdigest()
            return password_sha256 == self._users[username]
        return False

    def user_lookup(self, username):
        # The user_lookup method is optional and should return None if the user
        # does not have any permissions or roles that the backend is concerned with.
        return self._users.get(username)

# Middleware to handle authentication
class AuthMiddleware(FalconBasicAuthMiddleware):
    def __init__(self):
        super().__init__(BasicAuthBackend(), realm='Falcon API')

# The API resource
class SecureResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            if req.context.auth_info['authenticated'] == True:
                resp.body = b'Access granted'
                resp.status = falcon.HTTP_200
            else:
                raise Exception('Not authenticated')
        except Exception as e:
            raise falcon.HTTPUnauthorized('Authentication failed', str(e))

# Create the API
app = API()

# Add the middleware to the API
app.middleware.append(AuthMiddleware())

# Add a route and the resource
app.add_route('/secure', SecureResource())

# Run the API
if __name__ == '__main__':
    import falcon
    falcon.run(app, host='0.0.0.0', port=8000)
