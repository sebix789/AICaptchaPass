import pytest
from src.flaskr import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'
