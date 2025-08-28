# 代码生成时间: 2025-08-28 21:03:24
# batch_image_resizer.py
# A Falcon application for resizing images in batch

import falcon
from PIL import Image
from io import BytesIO
import os
from urllib.parse import urljoin, urlparse
import logging
from falcon import HTTP_500

# Configuration
API_VERSION = '/api/v1'
MEDIA_DIR = 'media'
OUTPUT_DIR = 'output'
RESIZED_SUFFIX = '_resized'
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']

class ImageResizer:
    """
    A Falcon resource class for resizing images.
    """
    def on_post(self, req, resp):
        # Check if the request body is empty
        if not req.bounded_stream:
            resp.status = falcon.HTTP_400
            resp.body = 'Empty request body.'
            return

        # Extract image file from the request body
        file_stream = req.bounded_stream
        image = None
        try:
            image = Image.open(file_stream)
        except IOError:
            raise falcon.HTTPError(falcon.HTTP_500, 'Invalid image format.')

        # Create an output directory if it does not exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # Define the output path for the resized image
        output_path = f'{OUTPUT_DIR}/{req.context[