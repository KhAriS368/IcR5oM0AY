# 代码生成时间: 2025-08-08 09:58:32
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
XSS Protection Service using Falcon framework.
This service provides basic protection against XSS attacks.
"""

import falcon
import html

def escape_html(text):  # Escape HTML special characters to prevent XSS
    """Escapes HTML special characters to prevent XSS attacks.

    Args:
        text (str): The text to be escaped.

    Returns:
        str: The escaped text.
    """
    return html.escape(text)

class XssProtectionResource:
    """A Falcon resource class that provides XSS protection."""
    def on_get(self, req, resp):
        """Handles GET requests.

        Args:
            req (falcon.Request): The incoming request.
            resp (falcon.Response): The outgoing response.
        """
        user_input = req.get_param('text', '')
        safe_text = escape_html(user_input)
        resp.media = {
            'original': user_input,
            'escaped': safe_text
        }

def create_app():
    """Creates the Falcon application."""
    app = falcon.App()
    app.add_route('/protect', XssProtectionResource())
    return app

if __name__ == '__main__':
    app = create_app()
    # You can use `pserve` to run this Falcon app:
    # pserve --server=falcon.asgi.ASGIServer xss_protection_service.py --reload
    # Alternatively, you can run it with a simple python server like:
    # python -m http.server 8000 --directory .
    # Make sure to set the `HOST` and `PORT` environment variables accordingly.
    from wsgiref import simple_server
    with simple_server.make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()