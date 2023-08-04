import pickle
import pandas as pd
from flask import Flask
from flask import request
import os
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin
from mlflow import MlflowClient
from pymongo import MongoClient
import mlflow
import requests
import pymongo
import json

app = Flask(__name__)

MLFLOW_TRACKING_URI = "https://dagshub.com/anagasperin/IIS_projekt.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()
run_id = client.get_latest_versions(
    'MLPRegressor', stages=['production'])[0].run_id
model = mlflow.pyfunc.load_model(f'runs:/{run_id}/MLPRegressor')

client = MongoClient('mongodb+srv://admin:admin@bikeavailability.xapwjao.mongodb.net/?retryWrites=true&w=majority')
db = client['IISProjekt']
collection = db['BikeAvailability']


def get_forecast():
    latitude = '46.55472' 
    longitude = '15.64667'

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation_probability,windspeed_10m'
    raw = requests.get(url)
    raw = raw.json()

    df = pd.DataFrame()
    df['hour'] = raw['hourly']['time']
    df['hour'] = pd.to_datetime(df['hour']).dt.hour

    df['temp'] = raw['hourly']['temperature_2m']
    df['temp'].fillna(df['temp'].mean(), inplace=True)
    df['temp'] = df['temp'].astype('float')

    df['hum'] = raw['hourly']['relativehumidity_2m']
    df['hum'].fillna(df['hum'].mean(), inplace=True)
    df['hum'] = df['hum'].astype('float')

    df['percp'] = raw['hourly']['precipitation_probability']
    df['percp'].fillna(df['percp'].mean(), inplace=True)
    df['percp'] = df['percp'].astype('float')

    df['wspeed'] = raw['hourly']['windspeed_10m']
    df['wspeed'].fillna(df['wspeed'].mean(), inplace=True)
    df['wspeed'] = df['wspeed'].astype('float')

    return df


@app.route('/forecast', methods=['GET'])
@cross_origin()
def forecast():
    df = get_forecast()

    df['capacity'] = 0
    df['capacity_free'] = 0

    print(df.columns)
    prediction = model.predict(df)
    df['vehicles_available'] = prediction
    df = df.head(72)

    df_dict = df.to_dict()
    json_data = {key: list(df_dict[key].values()) for key in df_dict}

    data = {
        'temp': df['temp'].tolist(),
        'hum': df['hum'].tolist(),
        'percp': df['percp'].tolist(),
        'wspeed': df['wspeed'].tolist(),
        'vehicles_available': df['vehicles_available'].tolist(),
        'hour': df['hour'].tolist(),
    }
    collection.insert_one(data)

    return json_data


def main():
    app.run(host='0.0.0.0', port=5000)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    main()