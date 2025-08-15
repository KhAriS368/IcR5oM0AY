# 代码生成时间: 2025-08-16 06:14:37
# uncompress_tool.py
# Python program to compress and decompress files using Falcon framework
# and the built-in zipfile module.

from falcon import API, Request, Response
import zipfile
import os
import io
import mimetypes

# Falcon API
class UncompressTool:
    def on_get(self, req, resp):
        # Respond with a simple plain-text message with the available endpoints.
        resp.media = {"message": "Use POST to decompress a file"}

    def on_post(self, req, resp):
        # Extract file from request
        try:
            file_stream, file_info = req.get_body()
            file_content = file_stream.read()
            
            # Save the file to a temporary location
            temp_file = io.BytesIO(file_content)
            
            # Create a ZipFile object to decompress the file
            with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                # Get the list of files in the zip archive
                zip_files = zip_ref.namelist()
                
                # Decompress each file into the current directory
                for file in zip_files:
                    # Extract file from the zip archive
                    zip_ref.extract(file)
                
                # Respond with a success message
                resp.media = {"message": "File decompressed successfully", "files": zip_files}
                resp.status = falcon.HTTP_200
            return
        except zipfile.BadZipFile:
            # Handle a bad zip file
            resp.media = {"error": "Invalid zip file provided"}
            resp.status = falcon.HTTP_400
        except Exception as e:
            # Handle any other exceptions
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_500

# Create Falcon API object
api = API()

# Add route for decompressing files
api.add_route('/', UncompressTool())

# The following code would be executed if the script is run as a script
# This is why it's wrapped in an if __name__ == "__main__": block
if __name__ == "__main__":
    # Run the Falcon API on localhost port 8000
    from wsgiref import simple_server
    httpd = simple_server.make_server("localhost", 8000, api)
    print("Serving on localhost port 8000...")
    httpd.serve_forever()