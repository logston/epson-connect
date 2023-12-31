import os

from .authenticate import AuthCtx
from .printer import Printer
from .scanner import Scanner


class Client:
    EC_BASE_URL = 'https://api.epsonconnect.com'

    def __init__(self, base_url='', printer_email='', client_id='', client_secret='') -> None:
        base_url = base_url or self.EC_BASE_URL

        printer_email = printer_email or os.environ.get('EPSON_CONNECT_API_PRINTER_EMAIL')
        if not printer_email:
            raise ClientError('Printer Email can not be empty')

        client_id = client_id or os.environ.get('EPSON_CONNECT_API_CLIENT_ID')
        if not client_id:
            raise ClientError('Client ID can not be empty')

        client_secret = client_secret or os.environ.get('EPSON_CONNECT_API_CLIENT_SECRET')
        if not client_secret:
            raise ClientError('Client Secret can not be empty')

        self._auth_ctx = AuthCtx(base_url, printer_email, client_id, client_secret)

    def deauthenticate(self):
        self._auth_ctx._deauthenticate()

    @property
    def printer(self):
        return Printer(self._auth_ctx)

    @property
    def scanner(self):
        return Scanner(self._auth_ctx)


class ClientError(ValueError):
    """
    General base error for any client specific errors.
    """
