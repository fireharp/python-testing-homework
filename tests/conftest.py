"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import pytest

from server.apps.identity.models import User

pytest_plugins = [
    # Should be the first custom one:
    'tests.plugins.django_settings',
    'tests.plugins.identity.user',
    'tests.plugins.pictures.picture',
]


@pytest.fixture()
@pytest.mark.django_db()
def authenticated_user(client):
    """Authenticated user."""  # noqa: D401
    user = User.objects.create_user(  # noqa:S106
        email='test@email.com', password='testpassword',
    )
    client.login(email='test@email.com', password='testpassword')  # noqa: S106
    return user


@pytest.fixture()
def unauthenticated_user():  # noqa: WPS324
    """Unauthenticated user."""
    return None  # noqa: WPS324
