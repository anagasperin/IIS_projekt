import pandas as pd
import mlflow
import os
import pymongo
from pymongo import MongoClient
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score


MLFLOW_TRACKING_URI = "https://dagshub.com/anagasperin/IIS_projekt.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("monitoring")

client = MongoClient('mongodb+srv://admin:admin@bikeavailability.xapwjao.mongodb.net/?retryWrites=true&w=majority')
db = client['IISProjekt']
collection = db['BikeAvailability']

def transform_categorical(column):
    print (column)
    vehicles_available = column['vehicles_available']
    # vehicles_available = vehicles_available.std.replace('<', '')
    nan_mask = vehicles_available.isna()
    vehicles_availablenan = vehicles_available[nan_mask]

    # vehicles_available = vehicles_available.std.strip().dropna().loc[lambda x: x.std.len() > 0]
    vehicles_available = vehicles_available.astype(int)

    vehicles_availablenan[:] = vehicles_available.mean()
    vehicles_available = pd.concat([vehicles_available, vehicles_availablenan], axis=0)

    column['vehicles_available'] = vehicles_available.astype(int)
    return column


def evaluate_predictions(bike_data):
    csv = pd.read_csv(bike_data, encoding='utf_8')
    df = pd.DataFrame(csv)

    vehicles_available = transform_categorical(df)
    df = vehicles_available

    data = collection.find()
    df1 = pd.DataFrame()

    df['date'] = pd.to_datetime(df['datetime']).dt.date
    df['hour'] = pd.to_datetime(df['datetime']).dt.hour

    for x in data:
        d = {'hour': x['hour'], 'y': x['vehicles_available']}
        tmp = pd.DataFrame(d)
        df1 = pd.concat([df1, tmp], axis=0)

    # df['hour'] = pd.to_datetime(df['hour'])
    # df1['hour'] = pd.to_datetime(df1['hour'])

    df = pd.merge(df1, df, on=['hour'], how='inner')
    df = df.drop_duplicates(subset=['hour'], keep='first')
    df = df.drop(columns='date')

    mse_test = mean_squared_error(df['vehicles_available'], df['y'])
    mae_test = mean_absolute_error(df['vehicles_available'], df['y'])
    evs_test = explained_variance_score(df['vehicles_available'], df['y'])

    mlflow.log_metric("MSE Test", mse_test)
    mlflow.log_metric("MAE Test", mae_test)
    mlflow.log_metric("EVS Test", evs_test)


def main():
    import os

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    bike_data = os.path.join(
        root_dir, 'data', 'processed', 'bike_data.csv')

    evaluate_predictions(bike_data)


if __name__ == '__main__':
    main()