import pandas as pd
import json
import os

def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    weather = os.path.join(root_dir, 'data', 'raw_weather', 'raw_weather_data.json')
    weather_proc = os.path.join(root_dir, 'data', 'processed', 'weather_data.csv')

    print('Processing weather data...')
    f = open(weather, 'r', encoding='utf-8')
    raw = json.load(f)
    f.close()

    df = pd.DataFrame()
    df['datetime'] = raw['hourly']['time']
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')

    df['temp'] = raw['hourly']['temperature_2m']
    df['temp'].fillna(df['temp'].mean(), inplace=True)

    df['hum'] = raw['hourly']['relativehumidity_2m']
    df['hum'].fillna(df['hum'].mean(), inplace=True)

    df['percp'] = raw['hourly']['precipitation']
    df['percp'].fillna(df['percp'].mean(), inplace=True)

    df['wspeed'] = raw['hourly']['windspeed_10m']
    df['wspeed'].fillna(df['wspeed'].mean(), inplace=True)

    print('Saving processed data...')
    df.to_csv(weather_proc, index=False)

if __name__ == '__main__':
    main()