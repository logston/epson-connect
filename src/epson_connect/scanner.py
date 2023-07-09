from .authenticate import AuthCtx


class Scanner:
    def __init__(self, auth_ctx: AuthCtx) -> None:
        self._auth_ctx = auth_ctx
        self._path = f'/api/1/scanning/scanners/{self._auth_ctx.device_id}/destinations'

    def list(self):
        """
        Get scan destinations.
        """
        method = 'GET'
        return self._auth_ctx.send(method, self._path)

    def add(self):
        """
        Register scan destination.
        """
        method = 'POST'
        return self._auth_ctx.send(method, self._path)

    def update(self):
        """
        Update scan destination.
        """
        method = 'POST'
        return self._auth_ctx.send(method, self._path)

    def remove(self):
        """
        Update scan destination.
        """
        method = 'DELETE'
        return self._auth_ctx.send(method, self._path)
