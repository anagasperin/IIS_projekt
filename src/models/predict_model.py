import pandas as pd
import pickle
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import mlflow


def predict_model(train_path, test_path, model_path, train_metrics_path, metrics_path):
    MLFLOW_TRACKING_URI = "https://dagshub.com/anagasperin/IIS_projekt.mlflow"
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("mlruns")
    mlflow.autolog()

    with mlflow.start_run():
        csv = pd.read_csv(train_path, encoding='utf_8')
        train = pd.DataFrame(csv)

        csv = pd.read_csv(test_path, encoding='utf_8')
        test = pd.DataFrame(csv)
        print('Data read')

        columns = np.array(train.columns)
        mask = columns != 'vehicles_available'
        x_train = train[columns[mask]]
        y_train = train['vehicles_available']
        x_test = test[columns[mask]]
        y_test = test['vehicles_available']

        model = LinearRegression()
        model.fit(x_train, y_train)
        print('Model trained')

        prediction = model.predict(x_test)

        # Calculate MSE and MAE for the test data
        mse_test = mean_squared_error(y_test, prediction)
        mae_test = mean_absolute_error(y_test, prediction)
        evs_test = explained_variance_score(y_test, prediction)

        mlflow.log_metric("MSE Test", mse_test)
        mlflow.log_metric("MAE Test", mae_test)
        mlflow.log_metric("EVS Test", evs_test)

        # Make predictions for the training data
        predictions_train = model.predict(x_train)

        # Calculate MSE and MAE for the training data
        mse_train = mean_squared_error(y_train, predictions_train)
        mae_train = mean_absolute_error(y_train, predictions_train)
        evs_train = explained_variance_score(y_train, predictions_train)

        mlflow.log_metric("MSE Train", mse_train)
        mlflow.log_metric("MAE Train", mae_train)
        mlflow.log_metric("EVS Train", evs_train)

        with open(train_metrics_path, 'w') as file:
            file.write('MAE:' + str(mae_train) + '\n')
            file.write('MSE:' + str(mse_train) + '\n')
            file.write('EVS:' + str(evs_train) + '\n')

        with open(metrics_path, 'w') as file:
            file.write('MAE:' + str(mae_test) + '\n')
            file.write('MSE:' + str(mse_test) + '\n')
            file.write('EVS:' + str(evs_test) + '\n')

        print('Reports updated')

        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        print('Model serialized')

        autolog_run = mlflow.last_active_run()
        print(autolog_run)


def main():
    import os

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    train_path = os.path.join(root_dir, 'data', 'processed', 'train.csv')
    test_path = os.path.join(root_dir, 'data', 'processed', 'test.csv')
    model_path = os.path.join(root_dir, 'models', 'linear')
    train_metrics_path = os.path.join(root_dir, 'reports', 'train_metrics.txt')
    metrics_path = os.path.join(root_dir, 'reports', 'metrics.txt')

    predict_model(train_path, test_path, model_path,
                  train_metrics_path, metrics_path)


if __name__ == '__main__':
    main()