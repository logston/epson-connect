import os
from unittest import mock

import pytest

from epson_connect.client import Client, ClientError
from epson_connect.printer import Printer
from epson_connect.scanner import Scanner


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
        'EPSON_CONNECT_API_PRINTER_EMAIL': 'epsonsample@print.epsonconnect.com',
        'EPSON_CONNECT_API_CLIENT_ID': 'abc',
        'EPSON_CONNECT_API_CLIENT_SECRET': '123',
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


def test_client_init_errors():
    with mock.patch.dict(os.environ, {
        'EPSON_CONNECT_API_CLIENT_ID': 'abc',
        'EPSON_CONNECT_API_CLIENT_SECRET': '123',
    }):
        with pytest.raises(ClientError) as e:
            Client()
        assert 'Printer Email can not be empty' in str(e)

    with mock.patch.dict(os.environ, {
        'EPSON_CONNECT_API_PRINTER_EMAIL': 'epsonsample@print.epsonconnect.com',
        'EPSON_CONNECT_API_CLIENT_SECRET': '123',
    }):
        with pytest.raises(ClientError) as e:
            Client()
        assert 'Client ID can not be empty' in str(e)

    with mock.patch.dict(os.environ, {
        'EPSON_CONNECT_API_PRINTER_EMAIL': 'epsonsample@print.epsonconnect.com',
        'EPSON_CONNECT_API_CLIENT_ID': 'abc',
    }):
        with pytest.raises(ClientError) as e:
            Client()
        assert 'Client Secret can not be empty' in str(e)


def test_client_deactivate(mocker):
    def mock_auth_ctx_send(
            self,
            *args,
            **kwargs,
    ):
        return {
            'refresh_token': 'rf-123',
            'expires_in': '3600',
            'access_token': 'at-5678',
            'subject_id': 'test_subj_id',
        }

    mocker.patch(
        'epson_connect.client.AuthCtx.send',
        mock_auth_ctx_send,
    )

    with mock.patch('epson_connect.client.AuthCtx._deauthenticate') as m:
        Client(
            base_url='https://example.com/my/path',
            printer_email='example2@print.epsonconnect.com',
            client_id='def',
            client_secret='456',
        ).deauthenticate()

    m.assert_called()


def test_client_printer(mocker):
    def mock_auth_ctx_send(
            self,
            *args,
            **kwargs,
    ):
        return {
            'refresh_token': 'rf-123',
            'expires_in': '3600',
            'access_token': 'at-5678',
            'subject_id': 'test_subj_id',
        }

    mocker.patch(
        'epson_connect.client.AuthCtx.send',
        mock_auth_ctx_send,
    )

    assert isinstance(Client(
        base_url='https://example.com/my/path',
        printer_email='example2@print.epsonconnect.com',
        client_id='def',
        client_secret='456',
    ).printer, Printer)


def test_client_scanner(mocker):
    def mock_auth_ctx_send(
            self,
            *args,
            **kwargs,
    ):
        return {
            'refresh_token': 'rf-123',
            'expires_in': '3600',
            'access_token': 'at-5678',
            'subject_id': 'test_subj_id',
        }

    mocker.patch(
        'epson_connect.client.AuthCtx.send',
        mock_auth_ctx_send,
    )

    assert isinstance(Client(
        base_url='https://example.com/my/path',
        printer_email='example2@print.epsonconnect.com',
        client_id='def',
        client_secret='456',
    ).scanner, Scanner)
