import os
import pytest
import ActivityMerger as am
import ActivityMerger.merge as merge

os.putenv('FLASK_ENV', 'development')


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.fixture
def client():
    client = am.app.test_client()
    return client

def test_merge_count(tmpdir):
    test_source = 'tests/fixtures/dfid/'
    output_file = tmpdir.join('temp_merge_test.xml')
    count = merge.merger(test_source, output_file)
    assert count == 620
