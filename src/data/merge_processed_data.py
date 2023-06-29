import pandas as pd
import os
from datetime import datetime

def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    bike_proc = os.path.join(root_dir, 'data', 'processed', 'bike_data.csv')
    weather_proc = os.path.join(root_dir, 'data', 'processed', 'weather_data.csv')
    output_file = os.path.join(root_dir, 'data', 'processed', 'current_data.csv')

    bike_df = pd.read_csv(bike_proc)
    weather_df = pd.read_csv(weather_proc)

    # bike_df['datetime'] = pd.to_datetime(bike_df['datetime'])
    bike_df['date'] = pd.to_datetime(bike_df['datetime']).dt.date
    bike_df['hour'] = pd.to_datetime(bike_df['datetime']).dt.hour

    # weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
    weather_df['date'] = pd.to_datetime(weather_df['datetime']).dt.date
    weather_df['hour'] = pd.to_datetime(weather_df['datetime']).dt.hour

    merged_data = bike_df.merge(weather_df, on=['date', 'hour'], how='inner')

    columns = ['date', 'hour', 'vehicles_available', 'temp', 'hum', 'percp', 'wspeed', 'capacity', 'capacity_free']
    merged_data = merged_data[columns]

    merged_data.to_csv(output_file, index=False)


if __name__ == '__main__':
    main()