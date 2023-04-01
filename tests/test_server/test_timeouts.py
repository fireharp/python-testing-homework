from http import HTTPStatus

import pytest
import requests

from server.settings.components.json_server import (
    JSON_SERVER_HOST,
    JSON_SERVER_PORT,
)


def test_external_service() -> None:
    """This test mocks some HTTP request."""
    response = requests.get(
        f'http://{JSON_SERVER_HOST}:{JSON_SERVER_PORT}/posts',  # noqa: WPS305
        timeout=(2, 5),
    )

    assert response.status_code == HTTPStatus.OK
    assert 'title' in response.json()[0]


@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_flaky_service() -> None:
    """This test ensures that unreliable service is accessible."""
    response = requests.get(
        'https://flaky.vercel.app/api/flaky',
        timeout=(1.5, 4),
    )

    assert response.status_code == HTTPStatus.OK
    assert 'message' in response.json()
