from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Client

from ..core import ApiError

class AuthClient:
    def __init__(self, client_wrapper: Client):
        self._client_wrapper = client_wrapper

    def login(self) -> None:
        response = self._client_wrapper.request(
            'login/validate',
            method='POST',
            data = {
                'username': self._client_wrapper.email,
                'password': self._client_wrapper.password
            }
        )

        if 200 <= response.status_code < 300:
            self._client_wrapper.cookies = response.cookies
        else:
            raise ApiError(response.status_code, response.text)


    def logout(self) -> None:
        response = self._client_wrapper.request(
            'logout',
            method = 'GET'
        )

        if response.status_code == 302:
            self._client_wrapper.cookies = None
        else:
            raise ApiError(response.status_code, response.text)