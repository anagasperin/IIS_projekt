import json
import os
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
import dvc.api

def main():
    # Fetch the data from the API
    response = requests.get("https://api.modra.ninja/jcdecaux/maribor/stations")
    data = response.json()

    # Convert the data to a DataFrame
    df = pd.json_normalize(data)

    # Set the timezone to GMT+2
    timezone = pytz.timezone('Europe/Berlin')

    # Create a filename based on the current datetime
    filename = datetime.now(timezone).strftime("%Y-%m-%d_%H-%M-%S.csv")

    # Define the DVC data directory
    dvc_data_dir = 'data/raw'

    # Create the raw data directory if it doesn't exist
    os.makedirs(dvc_data_dir, exist_ok=True)

    # Save the DataFrame to a CSV file in the DVC data directory
    file_path = os.path.join(dvc_data_dir, filename)
    df.to_csv(file_path, index=False)

    # Push the file to DVC
    dvc.api.push(file_paths=[file_path], remote='origin')

    # Remove the temporary file (optional since it's already in DVC)
    os.remove(file_path)

if __name__ == '__main__':
    main()
