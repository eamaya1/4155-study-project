from app import create_app
import pytest

def test_main(client):
    response = client.get('/')
    assert response.status == '200 OK'