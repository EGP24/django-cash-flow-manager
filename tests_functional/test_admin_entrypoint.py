import pytest


pytestmark = pytest.mark.functional


def test_admin_entrypoint_is_available(client):
    # act
    response = client.get('/admin/')

    # assert
    assert response.status_code == 302
    assert response.headers['Location'].startswith('/admin/login/')
