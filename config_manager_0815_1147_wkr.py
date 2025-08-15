# 代码生成时间: 2025-08-15 11:47:38
# config_manager.py

"""
Configuration Manager for Falcon Framework application
Handles loading and accessing configuration files in a structured manner
"""

import json
from falcon import Falcon, MediaHandler, HTTPBadRequest

# Define a class for managing configurations
class ConfigManager:
    def __init__(self, config_path):
        """Initialize the ConfigManager with a path to the configuration file"""
        self.config_path = config_path
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load the configuration from the file into memory"""
        try:
            with open(self.config_path, 'r') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            raise HTTPBadRequest('Configuration file not found', 'The configuration file is required')
        except json.JSONDecodeError:
            raise HTTPBadRequest('Invalid configuration format', 'The configuration file must be in valid JSON format')

    def get_config(self):
        """Return the loaded configuration dictionary"""
        return self.config

    def get_config_value(self, key, default=None):
        "