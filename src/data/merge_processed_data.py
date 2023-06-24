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

    # bike_df['hour'] = bike_df['date'].dt.hour
    # weather_df['hour'] = weather_df['date'].dt.hour

    merged_data = bike_df.merge(weather_df, on=['date', 'hour'], how='inner')

    merged_data = merged_data.drop(columns=['datetime_x', 'datetime_y', 'date'])

    merged_data.to_csv(output_file, index=False)

    # print('Merging data...')
    # csv = pd.read_csv(bike_proc, encoding='utf_8')
    # df = pd.DataFrame(csv)
    # # df = df.rename(columns={'datum_od': 'date'})

    # csv = pd.read_csv(weather_proc, encoding='utf_8')
    # df1 = pd.DataFrame(csv)

    # df['date'] = pd.to_datetime(df['date'])
    # df1['date'] = pd.to_datetime(df1['date'])

    # merged_df = pd.merge(df1, df, on='date', how='inner')
    # merged_df = merged_df.drop(columns='date')

    # print('Saving processed data...')
    # merged_df.to_csv(merged, index=False)

    # print('Finished!')


if __name__ == '__main__':
    main()