import pandas as pd
import mlflow
import os
import pymongo
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score


MLFLOW_TRACKING_URI = "https://dagshub.com/anagasperin/IIS_projekt.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("monitoring")

clientdb = pymongo.MongoClient(os.environ['MONGO_URI'])
db = clientdb.iis
col = db.prediction


def transform_categorical(column):
    pm10 = column['pm10']
    pm10 = pm10.str.replace('<', '')
    nan_mask = pm10.isna()
    pm10nan = pm10[nan_mask]

    pm10 = pm10.str.strip().dropna().loc[lambda x: x.str.len() > 0]
    pm10 = pm10.astype('float')

    pm10nan[:] = pm10.mean()
    pm10 = pd.concat([pm10, pm10nan], axis=0)

    column['pm10'] = pm10.astype('float')
    return column


def evaluate_predictions(data_air):
    csv = pd.read_csv(data_air, encoding='utf_8')
    df = pd.DataFrame(csv)

    pm10 = transform_categorical(df)
    pm10 = pm10.rename(columns={'datum_od': 'date', 'pm10': 't'})
    df = pm10

    data = col.find()
    df1 = pd.DataFrame()

    for x in data:
        d = {'date': x['date'], 'y': x['pm10']}
        tmp = pd.DataFrame(d)
        df1 = pd.concat([df1, tmp], axis=0)

    df['date'] = pd.to_datetime(df['date'])
    df1['date'] = pd.to_datetime(df1['date'])

    df = pd.merge(df1, df, on='date', how='inner')
    df = df.drop_duplicates(subset=['date'], keep='first')
    df = df.drop(columns='date')

    mse_test = mean_squared_error(df['t'], df['y'])
    mae_test = mean_absolute_error(df['t'], df['y'])
    evs_test = explained_variance_score(df['t'], df['y'])

    mlflow.log_metric("MSE Test", mse_test)
    mlflow.log_metric("MAE Test", mae_test)
    mlflow.log_metric("EVS Test", evs_test)


def main():
    import os

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    data_path = os.path.join(
        root_dir, 'data', 'preprocessed', 'data_air.csv')

    evaluate_predictions(data_path)


if __name__ == '__main__':
    main()