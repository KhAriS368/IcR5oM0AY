# 代码生成时间: 2025-08-09 07:18:32
# hash_calculator.py
# A simple hash calculator tool using Python and Falcon framework.

import falcon
import hashlib
import json
from falcon import HTTPBadRequest, HTTPInternalServerError

# Falcon API resource class for hash calculation
class HashCalculatorResource:
    def on_get(self, req, resp):
        """Handle GET requests to calculate hash."""
        try:
            # Get the input data from query parameters
            input_data = req.get_param('data', required=True)
            algorithm = req.get_param('algorithm', default='sha256')
            
            # Calculate the hash using the provided algorithm
            hash_result = self.calculate_hash(input_data, algorithm)
            
            # Return the hash result in JSON format
            resp.media = {'hash': hash_result}
            resp.status = falcon.HTTP_200
        except ValueError as e:
            # Handle invalid input data
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_400
        except Exception as e:
            # Handle any other unexpected errors
            resp.media = {'error': 'Internal server error'}
            resp.status = falcon.HTTP_500
    
    @staticmethod
    def calculate_hash(input_data, algorithm):
        """Calculate the hash of the input data using the specified algorithm."""
        try:
            # Create a new hash object
            hash_obj = getattr(hashlib, algorithm)()
            
            # Update the hash object with the input data
            hash_obj.update(input_data.encode('utf-8'))
            
            # Return the hexadecimal representation of the hash
            return hash_obj.hexdigest()
        except AttributeError:
            # Handle invalid hash algorithm
            raise ValueError(f'Unsupported hash algorithm: {algorithm}')
        except Exception as e:
            # Handle any other unexpected errors
            raise Exception(f'Error calculating hash: {str(e)}')

# Create a Falcon API app
app = falcon.App()

# Add the hash calculator resource to the app
app.add_route('/hash', HashCalculatorResource())