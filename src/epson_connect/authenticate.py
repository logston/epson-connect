import os
from datetime import datetime, timedelta

import requests
from requests.auth import HTTPBasicAuth


class AuthCtx:
    def __init__(
            self,
            base_url: str,
            printer_email: str,
            client_id: str,
            client_secret: str,
    ) -> None:
        self._base_url = base_url
        self._printer_email = printer_email
        self._client_id = client_id
        self._client_secret = client_secret

        self._expires_at = datetime.now()
        self._access_token = ''
        self._refresh_token = ''
        self._subject_id = ''

        self._auth()

    def _auth(self):
        method = 'POST'
        path = '/api/1/printing/oauth2/auth/token?subject=printer'

        if self._expires_at > datetime.now():
            return

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        auth = HTTPBasicAuth(self._client_id, self._client_secret)

        if self._access_token == '':
            data = {
                'grant_type': 'password',
                'username': self._printer_email,
                'password': '',
            }
        else:
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self._refresh_token,
            }

        try:
            body = self.send(method, path, data, headers=headers, auth=auth)
        except ApiError as e:
            raise AuthenticationError(e)

        error = body.get('error')
        if error:
            raise AuthenticationError(error)

        # First time authenticating, set refresh_token.
        if self._access_token == '':
            self._refresh_token = body['refresh_token']

        self._expires_at = datetime.now() + timedelta(seconds=int(body['expires_in']))
        self._access_token = body['access_token']
        self._subject_id = body['subject_id']

    def _deauthticate(self):
        """
        Cancel authentication.
        """
        method = 'DELETE'
        path = f'/api/1/printing/printers/{self._subject_id}'
        self.send(method, path)

    def send(self, method, path, data=None, headers=None, auth=None) -> dict:
        # auth is only set when we are authenticating with Client ID and Client Secret.
        # In this scenario, we do not want to call self._auth again as that
        # would cause a recursion exception.
        if not auth:
            self._auth()

        resp = requests.request(
            method=method,
            url=self._base_url + path,
            headers=headers or self.default_headers,
            data=data,
            auth=auth,
        ).json()

        error = resp.get('code')
        if error:
            raise ApiError(error)

        return resp

    @property
    def default_headers(self):
        return {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json',
        }

    @property
    def device_id(self):
        return self._subject_id


class AuthenticationError(RuntimeError):
    """
    Error for authentication specific exceptions.
    """


class ApiError(RuntimeError):
    """
    General base error for any API errors after authentication has succeeded.
    """


if __name__ == '__main__':
    # For testing.
    AuthCtx(
        base_url='https://api.epsonconnect.com',
        printer_email=os.environ['ESPON_CONNECT_API_PRINTER_EMAIL'],
        client_id=os.environ['ESPON_CONNECT_API_CLIENT_ID'],
        client_secret=os.environ['ESPON_CONNECT_API_CLIENT_SECRET'],
    )
