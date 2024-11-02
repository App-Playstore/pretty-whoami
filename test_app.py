import pytest
from app import app
import requests_mock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client, requests_mock):
    requests_mock.get('https://httpbin.org/get', text='Test Response')
    
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'Test Response' in response.data



