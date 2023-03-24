"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import pytest
from django.contrib.auth.models import User

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',

    # TODO: add your own plugins here!
]


@pytest.fixture()
def authenticated_user(client):
    """Creates a user and logs in."""
    user = User.objects.create_user(  # noqa:S106
        username='testuser', password='testpassword',
    )
    client.login(username='testuser', password='testpassword')  # noqa: S106
    return user


@pytest.fixture()
def unauthenticated_user():  # noqa: WPS324
    """Unauthenticated user."""
    return None  # noqa: WPS324
