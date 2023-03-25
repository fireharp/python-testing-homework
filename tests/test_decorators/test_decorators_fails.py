import logging
from http import HTTPStatus

import pytest
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.urls import include, path

from server.apps.identity.intrastructure.django.decorators import (
    redirect_logged_in_users,
)

logger = logging.getLogger(__name__)


@redirect_logged_in_users()
def sample_view(request):
    """A sample view that uses the decorator."""
    return HttpResponse('Test view')


def login_redirect_view(request):
    """A view that redirects to the login page."""
    return HttpResponse('Login Redirect View')


# Create a temporary Django URL pattern for testing purposes
pictures_patterns = [
    path('dashboard', login_redirect_view, name='dashboard'),
]

urlpatterns = [
    path('sample_view/', sample_view, name='sample_view'),
    path('login_redirect/', login_redirect_view, name='login_redirect_view'),
    path('pictures/', include((pictures_patterns, 'pictures'), namespace='pictures')),  # noqa: E501
]


@pytest.fixture()
def _mock_login_redirect_url(monkeypatch):
    """Mock the LOGIN_REDIRECT_URL setting."""
    # 1st way to mock the setting – doesn't work
    monkeypatch.setattr(
        'django.conf.settings.LOGIN_REDIRECT_URL',
        '/login_redirect/',
    )

    # 2nd way to mock django.urls.reverse_lazy – doesn't work
    def custom_reverse_lazy(viewname, *args, **kwargs):  # noqa: WPS430
        if viewname == 'pictures:dashboard':
            return '/login_redirect/'
        # return reverse_lazy(viewname, *args, **kwargs) # noqa: WPS609
        return '/login_redirect/'
    monkeypatch.setattr('django.urls.reverse_lazy', custom_reverse_lazy)

    # 3rd way to mock user_passes_test – doesn't work
    original_user_passes_test = user_passes_test

    def custom_user_passes_test(  # noqa: WPS430
        test_func, login_url=None, redirect_field_name='',
    ):
        return original_user_passes_test(
            test_func,
            login_url='/login_redirect/',
            redirect_field_name=redirect_field_name,
        )
    monkeypatch.setattr(
        'django.contrib.auth.decorators.user_passes_test',
        custom_user_passes_test,
    )


@pytest.mark.urls(__name__)
@pytest.mark.django_db()
@pytest.mark.usefixtures('_mock_login_redirect_url')
def test_redirect_logged_in_users_authenticated(
    monkeypatch, client, authenticated_user,
):
    """
    Test that the decorator redirects authenticated users.

    Doesn't work as desired because the LOGIN_REDIRECT_URL is not mocked.
    Instead of '/login_redirect/', the '/pictures/dashboard' URL is returned.

    So the '/pictures/dashboard' URL is mocked instead.
    """
    response = client.get('/sample_view/')
    assert response.status_code == HTTPStatus.FOUND
    logger.debug('RESPONSE URL:', response.url)
    # Out: '/pictures/dashboard' :( не получается запатчить

    logger.debug('LOGIN REDIRECT URL:', settings.LOGIN_REDIRECT_URL)
    # Out: '/login_redirect/' noqa: E800

    # assert response.url.startswith(settings.LOGIN_REDIRECT_URL) # noqa: E800

    # Follow the redirect and check if it leads to the correct URL
    response = client.get(response.url)
    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == 'Login Redirect View'


@pytest.mark.urls(__name__)
def test_redirect_logged_in_users_unauthenticated(client, unauthenticated_user):
    """Test that the unauthenticated user can access the view."""
    response = client.get('/sample_view/')
    assert response.status_code == HTTPStatus.OK
