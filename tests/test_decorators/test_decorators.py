
from http import HTTPStatus

import pytest
from django.urls import clear_url_caches


@pytest.mark.django_db()
@pytest.mark.skip(reason='This test is only passes when run separately.')
def test_redirect_logged_in_users_authenticated(
    settings, client, monkeypatch, authenticated_user,
):
    """
    Test that the authenticated user is redirected to the login redirect URL.

    Imports sequence is very important here,
    because we need to patch the decorator.
    """
    # prepare the proper redirect URL settings
    monkeypatch.setattr(
        'django.conf.settings.LOGIN_REDIRECT_URL', '/login_redirect/',
    )
    # import the sample app _after_ the settings are patched, otherwise it will
    # use the default settings
    import sample_app  # noqa: WPS433

    # _now_ we can do same thing pytest.mark.urls does, if we did it before
    # the import, it would be initialized with non-patched LOGIN_REDIRECT_URL
    settings.ROOT_URLCONF = sample_app
    clear_url_caches()

    # and finally we can test the view :)
    client.login(email='test@email.com', password='testpassword')  # noqa: S106

    response = client.get('/sample_view/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(settings.LOGIN_REDIRECT_URL)

    # Follow the redirect and check if it leads to the correct URL
    response = client.get(response.url)
    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == 'Login Redirect View'


@pytest.mark.urls('sample_app')
def test_redirect_logged_in_users_unauthenticated(client, unauthenticated_user):
    """Test that the unauthenticated user can access the view."""
    response = client.get('/sample_view/')
    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == 'Test view'
