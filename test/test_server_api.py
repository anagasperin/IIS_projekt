from src.server.server import app

def test_api_server():
    response = app.test_client().get('/forecast')
    assert response.status_code == 200