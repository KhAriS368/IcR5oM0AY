# 代码生成时间: 2025-08-14 18:40:06
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Cleaning and Preprocessing Tool using Falcon Framework
"""

from falcon import API, HTTP_200, HTTP_500, HTTP_400, HTTP_404
from falcon_cors import CORS
import pandas as pd
import numpy as np

# Initialize the Falcon API
app = API()

# CORS setup
cors = CORS(app)
cors.allowed_origins = ['*']
cors.allowed_methods = ['GET', 'POST']
cors.allowed_headers = ['Content-Type']

# Data cleaning functions
def clean_data(df):
    """
    Cleans the data by removing NaN values, duplicates, and outliers.
    :param df: pandas DataFrame containing the data to be cleaned.
    :return: Cleaned pandas DataFrame.
    """
    try:
        # Remove NaN values
        df_clean = df.dropna()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Remove outliers using IQR
        df_clean = df_clean[(np.abs(df_clean - df_clean.mean()) <= (3 * df_clean.std())).all(axis=1)]
        
        return df_clean
    except Exception as e:
        raise Exception(f"Error cleaning data: {str(e)}")

# Falcon Resource for data cleaning and preprocessing
class DataCleaningResource:
    def on_post(self, req, resp):
        """
        Handles POST requests to /clean endpoint for data cleaning.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        """
        try:
            # Get the JSON data from the request
            data = req.media.get('data')
            
            # Check if data is provided
            if not data:
                resp.status = HTTP_400
                resp.media = {'error': 'No data provided.'}
                return
            
            # Convert JSON data to pandas DataFrame
            df = pd.DataFrame(data)
            
            # Clean the data
            cleaned_df = clean_data(df)
            
            # Set the response status and media
            resp.status = HTTP_200
            resp.media = cleaned_df.to_dict(orient='records')
        except Exception as e:
            # Handle any exceptions and return a 500 error
            resp.status = HTTP_500
            resp.media = {'error': str(e)}

# Add the resource to the Falcon API
app.add_route('/clean', DataCleaningResource())

# Run the Falcon API
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)