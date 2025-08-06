# 代码生成时间: 2025-08-07 03:36:50
# batch_image_resizer.py
# A Falcon framework application for batch resizing images.

import os
# 添加错误处理
from falcon import API, Request, Response, HTTPBadRequest, HTTPInternalServerError
from PIL import Image

# Global configuration for image resizing
IMAGE_RESIZE_DEFAULT_SIZE = (800, 600)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class ImageResizer:
    """Handles image resizing functionality."""
    def __init__(self, resize_to=IMAGE_RESIZE_DEFAULT_SIZE):
        self.resize_to = resize_to

    def resize_image(self, image_path, output_path):
        """Resizes an image to the specified dimensions and saves it to the output path."""
        try:
            with Image.open(image_path) as img:
                img = img.resize(self.resize_to, Image.ANTIALIAS)
                img.save(output_path)
        except IOError as e:
            raise HTTPInternalServerError("Image resize failed", e)

    def batch_resize(self, directory, output_directory):
        """Resizes all images in the given directory and saves them to the output directory."""
# 扩展功能模块
        if not os.path.exists(output_directory):
# FIXME: 处理边界情况
            os.makedirs(output_directory)

        for filename in os.listdir(directory):
            if not filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
# FIXME: 处理边界情况
                continue
            image_path = os.path.join(directory, filename)
            output_path = os.path.join(output_directory, filename)
            self.resize_image(image_path, output_path)

class ImageResizerResource:
    """Falcon resource for batch resizing images."""
    def __init__(self):
        self.image_resizer = ImageResizer()

    def on_post(self, req, resp):
        "