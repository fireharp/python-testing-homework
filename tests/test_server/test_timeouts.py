from http import HTTPStatus

import pytest
import requests


def test_external_service() -> None:
    """This test ensures that unreliable service is accessible."""
    response = requests.get(
        'http://0.0.0.0:3000/posts',
        timeout=(2, 5),
    )

    assert response.status_code == HTTPStatus.OK
    assert 'title' in response.json()[0]


@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_flaky_service() -> None:
    """This test ensures that unreliable service is accessible."""
    response = requests.get(
        'https://flaky.vercel.app/api/flaky',
        timeout=(2, 5),
    )

    assert response.status_code == HTTPStatus.OK
    assert 'message' in response.json()
