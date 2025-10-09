# 代码生成时间: 2025-10-10 02:51:32
# keyboard_shortcut_handler.py

"""
A Falcon application that handles keyboard shortcuts.
"""
import falcon
from pynput import keyboard
from falcon import Request, Response

# Falcon's routing table
app = application = falcon.App()

# Define a resource to handle GET requests
class ShortcutResource:
    def on_get(self, req, resp):
        """Handles GET requests.

        Args:
            req: The incoming request object.
            resp: The outgoing response object.
        """
        resp.status = falcon.HTTP_200
        resp.media = {
            "message": "Keyboard shortcut handler is running"
        }

    # Define a method to handle POST requests for keyboard shortcuts
    def on_post(self, req, resp):
        """Handles POST requests to register keyboard shortcuts.

        Args:
            req: The incoming request object.
            resp: The outgoing response object.
        """
        try:
            # Parse the request body for the shortcut command and callback
            body = req.bounded_stream.read().decode('utf-8')
            shortcut_cmd = req.media.get('command')
            callback = req.media.get('callback')
            
            # Register the shortcut with the provided callback
            register_shortcut(shortcut_cmd, callback)
            
            resp.status = falcon.HTTP_200
            resp.media = {
                "message": "Shortcut registered successfully"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}

    # Define a method to handle DELETE requests for keyboard shortcuts
    def on_delete(self, req, resp):
        """Handles DELETE requests to unregister keyboard shortcuts.

        Args:
            req: The incoming request object.
            resp: The outgoing response object.
        """
        try:
            # Parse the request body for the shortcut command to unregister
            body = req.bounded_stream.read().decode('utf-8')
            shortcut_cmd = req.media.get('command')
            
            # Unregister the shortcut
            unregister_shortcut(shortcut_cmd)
            
            resp.status = falcon.HTTP_200
            resp.media = {
                "message": "Shortcut unregistered successfully"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}

# A list to store registered shortcuts and their callbacks
registered_shortcuts = []

# A function to register a keyboard shortcut
def register_shortcut(command, callback):
    """Registers a keyboard shortcut with a callback function.

    Args:
        command (str): The keyboard shortcut command.
        callback (function): The function to be called when the shortcut is pressed.
    """
    registered_shortcuts.append((command, callback))

    # Start listening for keyboard events if it hasn't already started
    if not keyboard.Listener(on_press=on_keypress).running:
        keyboard.Listener(on_press=on_keypress).start()

# A function to unregister a keyboard shortcut
def unregister_shortcut(command):
    """Unregisters a keyboard shortcut.

    Args:
        command (str): The keyboard shortcut command to unregister.
    """
    global registered_shortcuts
    registered_shortcuts = [(cmd, func) for cmd, func in registered_shortcuts if cmd != command]

# A function to handle keyboard presses
def on_keypress(key):
    """Handles keyboard press events.

    Args:
        key: The pressed key.
    """
    for command, callback in registered_shortcuts:
        if key == keyboard.KeyCode.from_char(command):
            callback()

# Add routes to the Falcon application
shortcut_resource = ShortcutResource()
app.add_route("/shortcut", shortcut_resource)

# Ensure the application runs when executed as a script
if __name__ == "__main__":
    import sys
    import socket
    from wsgiref.simple_server import make_server

    # Grab a port number from the command line, if given
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000

    # Create a server and run it
    httpd = make_server("", port, app)
    print("Serving on port %d...
    " % port)
    httpd.serve_forever()