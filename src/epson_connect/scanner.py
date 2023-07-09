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

    def add(self):
        """
        Register scan destination.
        """
        method = 'POST'

    def update(self):
        """
        Update scan destination.
        """
        method = 'POST'

    def remove(self):
        """
        Update scan destination.
        """
        method = 'DELETE'
