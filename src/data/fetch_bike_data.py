import json
import os
import pandas as pd
import requests
import time
from datetime import datetime




def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    
    save_path = os.path.join(root_dir, 'data', 'raw')

    # Fetch the data from the API
    response = requests.get("https://api.modra.ninja/jcdecaux/maribor/stations")
    data = response.json()

    # Convert the data to a DataFrame
    df = pd.json_normalize(data)

    # Create a filename based on the current datetime
    filename = os.path.join(save_path, datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv"))

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    main()