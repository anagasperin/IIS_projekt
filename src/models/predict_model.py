import os
import pandas as pd
import mlflow
import numpy as np
from mlflow import MlflowClient
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from mlflow.models.signature import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score

class CategoricalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return transform_categorical(X)
 
def transform_categorical(column):
    print (column)
    vehicles_available = column['vehicles_available']
    # vehicles_available = vehicles_available.std.replace('<', '')
    nan_mask = vehicles_available.isna()
    vehicles_availablenan = vehicles_available[nan_mask]

    # vehicles_available = vehicles_available.std.strip().dropna().loc[lambda x: x.std.len() > 0]
    vehicles_available = vehicles_available.astype('float')

    vehicles_availablenan[:] = vehicles_available.mean()
    vehicles_available = pd.concat([vehicles_available, vehicles_availablenan], axis=0)

    column['vehicles_available'] = vehicles_available.astype('float')
    return column

def transform_test(test_path, categorical_transform, numerical_transform):
    csv = pd.read_csv(test_path, encoding='utf_8')
    test = pd.DataFrame(csv)
    print('Data read')

    cat_features = test.select_dtypes(include=['object']).columns.tolist()
    num_features = test.select_dtypes(
        include=['float64', 'int64']).columns.tolist()

    test_preprocessor = ColumnTransformer([
        ('availability_transform', categorical_transform, cat_features),
        ('normal_transform', numerical_transform, num_features)
    ])

    arr = test_preprocessor.fit_transform(test)

    test = pd.DataFrame(
        arr, columns=["hour", "vehicles_available", "temp", "hum", "percp", "wspeed", "capacity", "capacity_free"])
    return test.astype('float')

def transform_test(test_path, categorical_transform, numerical_transform):
    csv = pd.read_csv(test_path, encoding='utf_8')
    test = pd.DataFrame(csv)
    print('Data read')

    cat_features = test.select_dtypes(include=['object']).columns.tolist()
    num_features = test.select_dtypes(
        include=['float64', 'int64']).columns.tolist()

    test_preprocessor = ColumnTransformer([
        ('availability_transform', categorical_transform, cat_features),
        ('normal_transform', numerical_transform, num_features)
    ])

    arr = test_preprocessor.fit_transform(test)
    test = pd.DataFrame(
        arr, columns=["hour", "vehicles_available", "temp", "hum", "percp", "wspeed", "capacity", "capacity_free"])
    return test

def train_model(train_path, test_path):
    MLFLOW_TRACKING_URI = "https://dagshub.com/anagasperin/IIS_projekt.mlflow"
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("mlruns")
    mlflow.autolog()

    csv = pd.read_csv(train_path, encoding='utf_8')
    train = pd.DataFrame(csv)

    x_train = train.drop('vehicles_available', axis=1)
    y_train = pd.DataFrame(train['vehicles_available'])

    num_features = ['temp', 'hum', 'percp', 'wspeed', 'hour', 'capacity', 'capacity_free']

    categorical_transform = Pipeline([
        ('transformer', CategoricalTransformer())
    ])

    arr = categorical_transform.fit_transform(y_train)
    y_train = pd.DataFrame(arr, columns=['vehicles_available'])

    numerical_transform = Pipeline([
        ('imputer', SimpleImputer(strategy='mean'))
    ])

    preprocessor = ColumnTransformer([
        ('numerical_transform', numerical_transform,
            num_features),
    ])

    pipe = Pipeline([
        ('preprocess', preprocessor),
        ('MLPR', MLPRegressor())
    ])

    parameter_space = {
        "MLPR__hidden_layer_sizes": [(32), (16)],
        "MLPR__learning_rate_init": [0.001, 0.01]
    }

    search = GridSearchCV(pipe, parameter_space,
                          verbose=2, error_score='raise')
    search.fit(x_train, y_train)

    test = transform_test(
        test_path, categorical_transform, numerical_transform)
    x_test = test.drop('vehicles_available', axis=1)
    y_test = pd.DataFrame(test['vehicles_available'])

    signature = infer_signature(x_train, search.predict(x_test))
    mlflow.sklearn.log_model(search, signature=signature, artifact_path="MLPRegressor",
                             registered_model_name="MLPRegressor")

    prediction = search.predict(x_test)

    # Calculate MSE and MAE for the test data
    mse_test = mean_squared_error(y_test, prediction)
    mae_test = mean_absolute_error(y_test, prediction)
    evs_test = explained_variance_score(y_test, prediction)

    mlflow.log_metric("MSE Test", mse_test)
    mlflow.log_metric("MAE Test", mae_test)
    mlflow.log_metric("EVS Test", evs_test)

    client = MlflowClient()
    m = client.get_latest_versions("MLPRegressor", stages=["Production"])[0]
    history = client.get_metric_history(m.run_id, "MAE Test")

    minM = history[0].value
    for h in history:
        if h.value < minM:
            minM = h.value

    if mae_test < minM:
        print("New best model")
        client.transition_model_version_stage(
            name="MLPRegressor", version=m.version, stage="Production",
        )


def main():
    import os

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    train_path = os.path.join(root_dir, 'data', 'processed', 'train.csv')
    test_path = os.path.join(root_dir, 'data', 'processed', 'test.csv')
    model_path = os.path.join(root_dir, 'models', 'linear')
    train_metrics_path = os.path.join(root_dir, 'reports', 'train_metrics.txt')
    metrics_path = os.path.join(root_dir, 'reports', 'metrics.txt')

    train_model(train_path, test_path
                #, model_path, train_metrics_path, metrics_path
                )


if __name__ == '__main__':
    main()