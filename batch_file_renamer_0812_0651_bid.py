# 代码生成时间: 2025-08-12 06:51:09
# batch_file_renamer.py
# A tool to batch rename files using Python and Falcon framework

import os
import re
from falcon import API, Request, Response
from falcon.asgi import ASGIAdapter
from falcon_cors import CORS
from argparse import ArgumentParser

# Falcon API instance
app = API()
cors = CORS(allow_all_origins=True)
app.add_hook(cors)

# Define the regex pattern for valid file names
VALID_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+$')

def rename_file(old_name, new_name):
    """ Rename a file from old_name to new_name. """
    if not VALID_FILENAME_PATTERN.match(new_name):
        raise ValueError('Invalid filename')

    old_path = os.path.join(os.getcwd(), old_name)
    new_path = os.path.join(os.getcwd(), new_name)

    try:
        os.rename(old_path, new_path)
    except FileNotFoundError:
        raise FileNotFoundError(f'The file {old_name} does not exist.')
    except PermissionError:
        raise PermissionError('Permission denied when trying to rename the file.')
    except OSError as e:
        raise OSError(f'Error renaming file: {e}')

class RenameResource:
    """ A Falcon resource to handle file renaming. """
    def on_post(self, req, resp):
        """ Handle POST requests to rename files. """
        try:
            body = req.media
            old_name = body.get('old_name')
            new_name = body.get('new_name')

            if not old_name or not new_name:
                raise ValueError('Both old_name and new_name are required.')

            rename_file(old_name, new_name)
            resp.media = {'message': 'File renamed successfully'}
            resp.status = falcon.HTTP_OK
        except (ValueError, FileNotFoundError, PermissionError, OSError) as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_BAD_REQUEST

# Register the resource
rename_resource = RenameResource()
app.add_route('/files/rename', rename_resource)

# Argument parser for command line interface
parser = ArgumentParser(description='Batch file renamer tool')
parser.add_argument('--host', type=str, default='localhost', help='Host address')
parser.add_argument('--port', type=int, default=8000, help='Port number')

# Run the Falcon API
if __name__ == '__main__':
    args = parser.parse_args()
    print(f'Starting Falcon API on {args.host}:{args.port}')
    adapter = ASGIAdapter(app)
    adapter.run(args.host, args.port)