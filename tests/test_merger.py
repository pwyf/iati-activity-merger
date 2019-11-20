import os
import pytest
import ActivityMerger as am

os.putenv('FLASK_ENV', 'development')


def test_assert():
    assert True


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.fixture
def client():
    client = am.app.test_client()
    return client
