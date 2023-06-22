import os
import csv
import json

output_data = []

# Assuming the CSV files are located in the 'data/raw/' directory
csv_directory = 'data/raw/'

for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        file_date = filename.split('.')[0]  # Extract the date from the file name
        with open(csv_directory + filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                # Assuming each row in the CSV file is a list of values
                # Modify this logic according to your actual CSV format
                data_entry = {
                    'date': file_date,
                    'values': row
                }
                output_data.append(data_entry)

# Write the merged data to a JSON file
output_file = 'data/bike/merged_bike_data.json'
with open(output_file, 'w') as json_file:
    json.dump(output_data, json_file)


