import csv
import os
import json

# Specify the directory where your CSV files are located
directory = 'data/raw/'

# Initialize the merged data list
merged_data = []

# Iterate over the CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        file_date = filename.split('.')[0]  # Extract the date from the file name

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Remove the 'type' and 'bbox' keys from the row dictionary
                row.pop('type', None)
                row.pop('bbox', None)

                # Create the data entry dictionary
                data_entry = {
                    'date': file_date,
                    'values': row
                }

                # Append the data entry to the merged data list
                merged_data.append(data_entry)

# Write the merged data to a JSON file
output_file = 'data/bike/merged_bike_data.json'
with open(output_file, 'w') as json_file:
    json.dump(merged_data, json_file)