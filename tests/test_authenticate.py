from datetime import datetime, timedelta
from unittest import mock

import pytest
import requests

from epson_connect.authenticate import ApiError, AuthCtx, AuthenticationError


def test_auth_ctx(mocker):
    def mock_send_one(
            self,
            method,
            path,
            data=None,
            headers=None,
            auth=None,
    ):
        assert method == 'POST'
        assert path == '/api/1/printing/oauth2/auth/token?subject=printer'
        assert data == {
            'grant_type': 'password',
            'password': '',
            'username': 'example3@print.epsonconnect.com',
        }
        assert headers == {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        assert auth is not None
        assert auth.username == 'ghi'
        assert auth.password == '789'

        return {
            'refresh_token': 'rf-123',
            'expires_in': '3600',
            'access_token': 'at-5678',
            'subject_id': 'test_subj_id',
        }

    mocker.patch(
        'epson_connect.authenticate.AuthCtx.send',
        mock_send_one,
    )

    auth_ctx = AuthCtx(
        base_url='https://example.com/my/path',
        printer_email='example3@print.epsonconnect.com',
        client_id='ghi',
        client_secret='789',
    )

    # Second access with expired token
    def mock_send_two(
            self,
            method,
            path,
            data=None,
            headers=None,
            auth=None,
    ):
        assert method == 'POST'
        assert path == '/api/1/printing/oauth2/auth/token?subject=printer'
        assert data == {
            'grant_type': 'refresh_token',
            'refresh_token': 'rf-123',
        }
        assert headers == {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        assert auth is not None
        assert auth.username == 'ghi'
        assert auth.password == '789'

        return {
            'refresh_token': 'rf-123',
            'expires_in': '3600',
            'access_token': 'at-5678',
            'subject_id': 'test_subj_id',
        }

    mocker.patch(
        'epson_connect.authenticate.AuthCtx.send',
        mock_send_two,
    )

    # Expire token.
    auth_ctx._expires_at = datetime.now()
    auth_ctx._auth()

    # Set unexpired token.
    auth_ctx._expires_at = datetime.now() + timedelta(seconds=10)

    with mock.patch('epson_connect.authenticate.AuthCtx.send') as m:
        m.return_value = {}
        auth_ctx._auth()

    m.assert_not_called()


def test_auth_ctx_api_to_auth_error():
    with mock.patch('epson_connect.authenticate.AuthCtx.send') as m:
        m.side_effect = AuthenticationError('test')

        with pytest.raises(AuthenticationError):
            AuthCtx(
                base_url='https://example.com/my/path',
                printer_email='example3@print.epsonconnect.com',
                client_id='ghi',
                client_secret='789',
            )


def test_auth_ctx_api_error():
    with mock.patch('epson_connect.authenticate.AuthCtx.send') as m:
        m.return_value = {'error': 'test'}

        with pytest.raises(AuthenticationError):
            AuthCtx(
                base_url='https://example.com/my/path',
                printer_email='example3@print.epsonconnect.com',
                client_id='ghi',
                client_secret='789',
            )


@mock.patch('epson_connect.authenticate.AuthCtx._auth')
@mock.patch('requests.request')
def test_auth_ctx_send_status_ok(req, _auth):
    mock_resp = requests.Response()
    mock_resp.encoding = 'utf8'
    mock_resp._content = b'{"status": "ok"}'
    req.return_value = mock_resp

    auth_ctx = AuthCtx(
        base_url='https://example.com/my/path',
        printer_email='example3@print.epsonconnect.com',
        client_id='ghi',
        client_secret='789',
    )

    auth_ctx.send('test_method', 'test_path')

    _auth.assert_called()


@mock.patch('epson_connect.authenticate.AuthCtx._auth')
@mock.patch('requests.request')
def test_auth_ctx_send_api_error(req, _auth):
    mock_resp = requests.Response()
    mock_resp.encoding = 'utf8'
    mock_resp._content = b'{"code": "test api problems"}'
    req.return_value = mock_resp

    auth_ctx = AuthCtx(
        base_url='https://example.com/my/path',
        printer_email='example3@print.epsonconnect.com',
        client_id='ghi',
        client_secret='789',
    )

    with pytest.raises(ApiError) as e:
        auth_ctx.send('test_method', 'test_path')

    assert 'test api problems' in str(e)
    _auth.assert_called()


@mock.patch('epson_connect.authenticate.AuthCtx._auth')
@mock.patch('requests.request')
def test_auth_ctx_send_non_json_response(req, _auth):
    mock_resp = requests.Response()
    mock_resp.encoding = 'utf8'
    mock_resp._content = b'something not json'
    req.return_value = mock_resp

    auth_ctx = AuthCtx(
        base_url='https://example.com/my/path',
        printer_email='example3@print.epsonconnect.com',
        client_id='ghi',
        client_secret='789',
    )

    with pytest.raises(ApiError) as e:
        auth_ctx.send('test_method', 'test_path')

    assert 'something not json' in str(e)
    _auth.assert_called()


@mock.patch('epson_connect.authenticate.AuthCtx._auth')
def test_auth_ctx_default_headers(_auth):
    auth_ctx = AuthCtx(
        base_url='https://example.com/my/path',
        printer_email='example3@print.epsonconnect.com',
        client_id='ghi',
        client_secret='789',
    )

    auth_ctx._access_token = 'abc123'

    assert auth_ctx.default_headers == {
        'Authorization': 'Bearer abc123',
        'Content-Type': 'application/json',
    }
