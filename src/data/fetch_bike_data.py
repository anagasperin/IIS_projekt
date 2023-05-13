import json
import os
import pandas as pd
import requests
import time
from datetime import datetime

root_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..'))
save_path = os.path.join(root_dir, 'data', 'raw')


    # print('Fetching air data...')
    # url = "https://api.modra.ninja/jcdecaux/maribor/stations"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     print("Fetched main datset")
    #     data = json.loads(response.content)
    #     with open(air, "w") as f:
    #         json.dump(data, f)
    # else:
    #     print("Failed to retrieve JSON data")

while True:
    # Fetch the data from the API
    response = requests.get("https://api.modra.ninja/jcdecaux/maribor/stations")
    data = response.json()

    # Convert the data to a DataFrame
    df = pd.json_normalize(data)

    # Create a filename based on the current datetime
    filename = os.path.join(save_path, datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv"))

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)