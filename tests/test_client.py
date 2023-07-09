import os
from unittest import mock

from epson_connect.client import Client


def test_client_init(mocker):
    def mock_auth_ctx_init(
            self,
            base_url: str,
            printer_email: str,
            client_id: str,
            client_secret: str,
    ) -> None:
        assert base_url == 'https://example.com/my/path'
        assert printer_email == 'example2@print.epsonconnect.com'
        assert client_id == 'def'
        assert client_secret == '456'

    mocker.patch(
        'epson_connect.client.AuthCtx.__init__',
        mock_auth_ctx_init,
    )

    Client(
        base_url='https://example.com/my/path',
        printer_email='example2@print.epsonconnect.com',
        client_id='def',
        client_secret='456',
    )


def test_client_init_env_vars(mocker):
    # Mocker does not support mocking os.environ, so we fall back to std library here.
    with mock.patch.dict(os.environ, {
        'ESPON_CONNECT_API_PRINTER_EMAIL': 'epsonsample@print.epsonconnect.com',
        'ESPON_CONNECT_API_CLIENT_ID': 'abc',
        'ESPON_CONNECT_API_CLIENT_SECRET': '123',
        }):

        def mock_auth_ctx_init(
                self,
                base_url: str,
                printer_email: str,
                client_id: str,
                client_secret: str,
        ) -> None:
            assert base_url == Client.EC_BASE_URL
            assert printer_email == 'epsonsample@print.epsonconnect.com'
            assert client_id == 'abc'
            assert client_secret == '123'

        mocker.patch(
            'epson_connect.client.AuthCtx.__init__',
            mock_auth_ctx_init,
        )

        Client()
