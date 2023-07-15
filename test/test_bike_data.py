import requests


def test_bike_api():
    url = "https://api.modra.ninja/jcdecaux/maribor/stations"
    response = requests.get(url)
    assert response.status_code == 200