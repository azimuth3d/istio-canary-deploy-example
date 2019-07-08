import pytest
import app

@pytest.fixture
def client():
    client = app.app.test_client()
    yield client


def test_version(client):
    req = client.get('/')
    assert req.data == app.version