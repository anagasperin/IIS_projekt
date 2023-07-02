import json
import requests
import datetime
import os
import tempfile

def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    
    weather = os.path.join(root_dir, 'data', 'raw_weather', 'raw_weather_data.json')
    os.makedirs(weather, exist_ok=True)

    with tempfile.TemporaryDirectory() as weather:
        print('Fetching weather data...')
        # Get the current date and time
        current_date = datetime.datetime.now()

        # Get the date one month ago
        one_month_ago = current_date - datetime.timedelta(days=60)

        # Convert dates to Unix time
        current_unix_time = int(current_date.timestamp())
        one_month_ago_unix_time = int(one_month_ago.timestamp())

        latitude = '46.55472' 
        longitude = '15.64667'

        end_date = datetime.datetime.utcfromtimestamp(
            current_unix_time).strftime('%Y-%m-%d')
        start_date = datetime.datetime.utcfromtimestamp(
            one_month_ago_unix_time).strftime('%Y-%m-%d')

        url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relativehumidity_2m,precipitation,windspeed_10m'
        response = requests.get(url)
        if response.status_code == 200:
            print("Fetched weather history")
            data = json.loads(response.content)
            with open(weather, "w") as f:
                json.dump(data, f)
        else:
            print("Failed to retrieve JSON data")

if __name__ == '__main__':
    main()