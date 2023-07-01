import pickle
import pandas as pd
from flask import Flask
from flask import request
import os
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)


def get_forecast():
    latitude = '46.55472' 
    longitude = '15.64667'

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation_probability,windspeed_10m'
    raw = requests.get(url)
    raw = raw.json()

    df = pd.DataFrame()
    df['date'] = raw['hourly']['time']
    df['date'] = pd.to_datetime(df['date'])

    df['temp'] = raw['hourly']['temperature_2m']
    df['temp'].fillna(df['temp'].mean(), inplace=True)

    df['hum'] = raw['hourly']['relativehumidity_2m']
    df['hum'].fillna(df['hum'].mean(), inplace=True)

    df['percp'] = raw['hourly']['precipitation_probability']
    df['percp'].fillna(df['percp'].mean(), inplace=True)

    df['wspeed'] = raw['hourly']['windspeed_10m']
    df['wspeed'].fillna(df['wspeed'].mean(), inplace=True)

    df['capacity'] = raw['hourly']['capacity']
    df['capacity'].fillna(df['capacity'].mean(), inplace=True)

    df['capacity_free'] = raw['hourly']['capacity_free']
    df['capacity_free'].fillna(df['capacity_free'].mean(), inplace=True)

    df['hour'] = raw['hourly']['hour']
    df['hour'].fillna(df['hour'].mean(), inplace=True)

    return df


@app.route('/forecast', methods=['GET'])
@cross_origin()
def forecast():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    model_path = os.path.join(root_dir, 'models', 'linear')

    f = open(model_path, 'rb')
    model = pickle.load(f)

    df = get_forecast()
    df_date = pd.to_datetime(df['date'])
    df_date = df_date.dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df.drop(columns='date')

    prediction = model.predict(df)
    df['vehicles_available'] = prediction
    df['date'] = df_date
    df = df.head(72)

    df_dict = df.to_dict()
    json_data = {key: list(df_dict[key].values()) for key in df_dict}

    return json_data


def main():
    app.run(host='0.0.0.0', port=5000)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    main()