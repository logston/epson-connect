from .authenticate import AuthCtx


class Scanner:
    VALID_DESTINATION_TYPES = {
        'mail',
        'url',
    }

    def __init__(self, auth_ctx: AuthCtx) -> None:
        self._auth_ctx = auth_ctx
        self._path = f'/api/1/scanning/scanners/{self._auth_ctx.device_id}/destinations'
        self._destination_cache = {}

    def list(self):
        """
        Get scan destinations.
        """
        method = 'GET'
        return self._auth_ctx.send(method, self._path)

    def add(self, name, destination, type_='mail'):
        """
        Register scan destination.
        """
        method = 'POST'

        self._validate_destination(name, destination, type_)

        data = {
            'alias_name': name,
            'type': type_,
            'destination': destination,
        }

        resp = self._auth_ctx.send(method, self._path, data)
        self._destination_cache[resp['id']] = resp
        return resp

    def update(self, id_, name=None, destination=None, type_=None):
        """
        Update scan destination.
        """
        method = 'POST'

        dest_cache = self._destination_cache.get(id_)
        if dest_cache is None:
            raise ScannerError('Scan destination is not yet registered.')

        self._validate_destination(name, destination, type_)

        data = {
            'id': id_,
            'alias_name': name if name else dest_cache['alias_name'],
            'type': type_ if type_ else dest_cache['type'],
            'destination': destination if destination else dest_cache['destination'],
        }

        resp = self._auth_ctx.send(method, self._path, data)
        self._destination_cache[id_] = resp
        return resp

    def remove(self, id_):
        """
        Update scan destination.
        """
        method = 'DELETE'

        data = {
            'id': id_,
        }

        self._auth_ctx.send(method, self._path, data)

        del self._destination_cache[id_]

    def _validate_destination(self, name, destination, type_):
        if len(name) < 1 or len(name) > 32:
            raise ScannerError('Scan destination name too long.')

        if len(destination) < 4 or len(destination) > 544:
            raise ScannerError('Scan destination too long.')

        if type_ not in self.VALID_DESTINATION_TYPES:
            raise ScannerError(f'Invalid scan destination type {type_}.')


class ScannerError(ValueError):
    pass
