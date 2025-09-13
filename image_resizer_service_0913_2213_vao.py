# 代码生成时间: 2025-09-13 22:13:41
# image_resizer_service.py

"""
A Falcon service for batch resizing images.
"""
# 改进用户体验

import falcon
import os
from PIL import Image

class ImageResizer:
    """
    A class to handle image resizing.
    """
    def __init__(self, output_folder):
        self.output_folder = output_folder
# NOTE: 重要实现细节

    def resize(self, input_folder, output_folder, new_size):
        """
        Resize images in the input folder and save them to the output folder.
        
        :param input_folder: The directory containing the original images.
        :param output_folder: The directory where resized images will be saved.
        :param new_size: A tuple containing the new width and height.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    with Image.open(os.path.join(input_folder, filename)) as img:
                        img = img.resize(new_size, Image.ANTIALIAS)
# NOTE: 重要实现细节
                        img.save(os.path.join(output_folder, filename))
                except IOError as e:
                    print(f"Error resizing {filename}: {e}")

    @staticmethod
    def validate_params(req, resp, resource, params):
        """
        Validate request parameters.
        """
        if 'new_size' not in params or 'input_folder' not in params or 'output_folder' not in params:
            raise falcon.HTTPBadRequest('Missing required parameters', 'new_size, input_folder, and output_folder are required.')

        # Check if new_size is a tuple of two integers
        try:
            new_size = tuple(int(x) for x in params['new_size'].split(','))
        except (ValueError, TypeError):
# NOTE: 重要实现细节
            raise falcon.HTTPBadRequest('Invalid new_size format', 'new_size must be a comma-separated pair of integers.')

        # Check if folders exist
# 优化算法效率
        if not os.path.isdir(params['input_folder']) or not os.path.isdir(params['output_folder']):
            raise falcon.HTTPBadRequest('Invalid folder paths', 'Both input_folder and output_folder must be valid directories.')

    @staticmethod
    def on_post(req, resp, resource):
        """
        Handle POST request to resize images.
# 扩展功能模块
        """
        # Get parameters from the query string
        params = req.params
        ImageResizer.validate_params(req, resp, resource, params)

        # Instantiate the ImageResizer and resize images
        resizer = ImageResizer(params['output_folder'])
        resizer.resize(params['input_folder'], params['output_folder'], (new_size[0], new_size[1]))

        # Return a success message
        resp.media = {'message': 'Images resized successfully.'}

# Create a Falcon API
app = falcon.API()

# Add a route for resizing images
resize_resource = falcon.Resource()
app.add_route('/images/resize', resize_resource)
