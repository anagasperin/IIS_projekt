import pandas as pd
import json
import os


def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    bike = os.path.join(root_dir, 'data', 'bike', 'merged_bike_data.json')
    bike_proc = os.path.join(root_dir, 'data', 'bike', 'processed_bike_data.csv')

    print('Processing bike data...')

    f = open(bike, 'r', encoding='utf-8')
    raw = json.load(f)
    f.close()

    df = pd.DataFrame()

    print('Json to data frame...')
    # prilagodimo json dataframe-u
    filtered_data = []
    for i in range(len(raw)):
        jdata = json.loads(raw[i]['values'])
        station = jdata['properties']['title']
        date = raw[i]['date']
        if i in range(len(station)):
            if station[i]['title'] == 'GOSPOSVETSKA C. - III. GIMNAZIJA':
                data = station[i]
                df = pd.concat([df, pd.json_normalize(data)])
    return filtered_data


if __name__ == '__main__':
    main()

    #{'type': 'Feature', 'geometry': {'coordinates': [15.64053, 46.560761], 'type': 'Point'}, 'properties': {'system': 'maribor', 'provider': 'europlakat', 'type': 'bike_station', 'id': '3', 'title': 'GOSPOSVETSKA C. - III. GIMNAZIJA', 'image_url': None, 'capacity': 20, 'vehicles_available': 18, 'capacity_free': 2, 'address': None}, 'id': '3', 'bbox': None}