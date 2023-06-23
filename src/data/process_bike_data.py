from datetime import datetime
import pandas as pd
import json
import os

def filter_stations_by_title(stations, title):
    filtered_stations = []
    for station in stations:
        features_str = station['values']
        features_str = features_str.replace("'", '\"')
        features_str = features_str.replace("None", "\"NULL\"")

        features_list = json.loads(features_str)
    
        for feature in features_list:
            station_title = feature['properties']['title']

            if title in station_title:
                parsed_date = datetime.strptime(station['date'], "%Y-%m-%d_%H-%M-%S")
                station['date'] = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

                filtered_stations.append(station)
    
    return filtered_stations

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    bike = os.path.join(root_dir, 'data', 'bike', 'merged_bike_data.json')
    bike_proc = os.path.join(root_dir, 'data', 'bike', 'processed_bike_data.csv')

    # Create a dataframe with filtered stations and the columns of interest
    with open(bike, 'r', encoding='utf-8') as json_file:  # Specify the encoding as 'utf-8'
        data = json.loads(json_file.read())

        filtered_stations = filter_stations_by_title(data, 'GOSPOSVETSKA C. - III. GIMNAZIJA')

        df = pd.DataFrame(filtered_stations)
        df = df.reset_index(drop=True)
        df['time'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
        df = df[['time', 'capacity', 'vehicles_available', 'capacity_free']]
        df.to_csv(bike_proc, index=False)

if __name__ == '__main__':
    main()