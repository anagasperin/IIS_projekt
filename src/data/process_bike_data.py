import pandas as pd
import json
import os


def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    bike = os.path.join(root_dir, 'data', 'bike', 'merged_bike_data.json')
    bike_proc = os.path.join(root_dir, 'data', 'bike', 'processed_bike_data.csv')

    print('Processing bike data...')

    f = open(bike, 'r', encoding='utf-8')
    raw = json.load(f)
    f.close()

    df = pd.DataFrame()

    print('Json to data frame...')

    for item in raw:
        jdata = item['values']
        features = jdata['FeatureCollection']['properties']['title']

        if 'title' in features and features['title'] == 'GOSPOSVETSKA C. - III. GIMNAZIJA':
            date = item['date']
            capacity = features['capacity']
            vehicles_available = features['vehicles_available']
            capacity_free = features['capacity_free']

            df = df.append({'date': date, 'capacity': capacity, 'vehicles_available': vehicles_available, 'capacity_free': capacity_free}, ignore_index=True)
                
    df.to_csv(bike_proc, index=False)
if __name__ == '__main__':
    main()

    #{'type': 'Feature', 'geometry': {'coordinates': [15.64053, 46.560761], 'type': 'Point'}, 'properties': {'system': 'maribor', 'provider': 'europlakat', 'type': 'bike_station', 'id': '3', 'title': 'GOSPOSVETSKA C. - III. GIMNAZIJA', 'image_url': None, 'capacity': 20, 'vehicles_available': 18, 'capacity_free': 2, 'address': None}, 'id': '3', 'bbox': None}