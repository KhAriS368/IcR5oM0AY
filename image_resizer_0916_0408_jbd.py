# 代码生成时间: 2025-09-16 04:08:35
 * Requirements:
 * - falcon: A high-performance cloud API framework for Python.
# 扩展功能模块
 * - PIL (Pillow): Python Imaging Library for image processing.
 *
 * Usage:
 * - This application provides an endpoint to accept image resizing requests.
 * - The request should include the target width and height.
 * - The program will read image files from a specified directory and resize them.
# NOTE: 重要实现细节
 */

import falcon
from PIL import Image
import os
# FIXME: 处理边界情况
import io
import mimetypes

# Define a class for image resizing resource
class ImageResizer:
    def __init__(self, target_width, target_height):
        self.target_width = target_width
        self.target_height = target_height

    def on_get(self, req, resp):
        # Check if the required parameters are provided
        try:
            target_width = int(req.get_param("width"))
# FIXME: 处理边界情况
            target_height = int(req.get_param("height"))
        except (TypeError, ValueError):
            raise falcon.HTTPBadRequest('Invalid width or height parameters')

        # Initialize the response
        resp.status = falcon.HTTP_200
        resp.content_type = "text/plain"

        # Get the directory path from the query parameter
        directory_path = req.get_param('directory')
        if not directory_path:
# 增强安全性
            raise falcon.HTTPBadRequest('Directory parameter is missing')

        # Check if the directory exists
        if not os.path.isdir(directory_path):
            raise falcon.HTTPNotFound('The specified directory does not exist')

        # Iterate through each file in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
# NOTE: 重要实现细节
            if os.path.isfile(file_path):
# 增强安全性
                try:
                    # Open and resize the image
                    with Image.open(file_path) as img:
# 改进用户体验
                        resized_img = img.resize((target_width, target_height), Image.ANTIALIAS)
                        # Save the resized image
                        resized_img.save(file_path)
                        print(f"Resized {filename} to {target_width}x{target_height}")
                except IOError:
                    print(f"Failed to process {filename}")

    # Define the on_options method to handle OPTIONS requests for CORS
    def on_options(self, req, resp):
        resp.status = falcon.HTTP_200
# NOTE: 重要实现细节
        allow_origin = req.get_header('Access-Control-Allow-Origin')
        resp.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
# FIXME: 处理边界情况
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        if allow_origin:
# NOTE: 重要实现细节
            resp.set_header('Access-Control-Allow-Origin', allow_origin)

# Falcon API setup
api = application = falcon.API()

# Add the '/image_resizer' route with the ImageResizer resource
api.add_route("/image_resizer", ImageResizer(target_width=800, target_height=600))
