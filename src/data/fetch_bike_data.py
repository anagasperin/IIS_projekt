import json
import os
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
import tempfile

def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    
    save_path = os.path.join(root_dir, 'data', 'raw')

    with tempfile.TemporaryDirectory() as temp_dir:
        # Fetch the data from the API
        response = requests.get("https://api.modra.ninja/jcdecaux/maribor/stations")
        data = response.json()

        # Convert the data to a DataFrame
        df = pd.json_normalize(data)

        # Set the timezone to GMT+2
        timezone = pytz.timezone('Europe/Berlin')
        
        # Create a filename based on the current datetime
        filename = os.path.join(save_path, datetime.now(timezone).strftime("%Y-%m-%d_%H-%M-%S.csv"))

        save_path = os.path.join(temp_dir, filename)
        # Save the DataFrame to a CSV file
        df.to_csv(save_path, index=False)

        save_dir = os.path.join('data', 'raw')
        os.makedirs(save_dir, exist_ok=True)

        # Move the file to the 'data/raw' directory
        final_path = os.path.join(save_dir, filename)
        os.rename(save_path, final_path)

if __name__ == '__main__':
    main()