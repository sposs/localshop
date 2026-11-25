import pytest

from tests.factories import UserFactory


@pytest.mark.django_db
def test_logout_requires_post(client):
    # Django 5.0 removed GET support from LogoutView.
    client.force_login(UserFactory())

    response = client.get('/dashboard/')
    assert b'method="post" action="/accounts/logout/"' in response.content

    response = client.post('/accounts/logout/')
    assert response.status_code in (200, 302)
    assert '_auth_user_id' not in client.session
