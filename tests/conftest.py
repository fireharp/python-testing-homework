"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import random

import pytest

pytest_plugins = [
    # Should be the first custom one:
    'tests.plugins.django_settings',
    'tests.plugins.identity.user',
    'tests.plugins.pictures.picture',
]

SEED_LENGTH = 32


@pytest.fixture()
def faker_seed():
    """Generates random seed."""
    return random.Random().getrandbits(SEED_LENGTH)
