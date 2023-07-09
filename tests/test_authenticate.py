from datetime import datetime
from epson_connect.authenticate import AuthCtx


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
