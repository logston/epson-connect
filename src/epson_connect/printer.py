import pathlib
from urllib.parse import parse_qs, urlencode, urlparse

from .authenticate import AuthCtx
from .printer_settings import merge_with_default_settings, validate_settings


class Printer:
    VALID_EXTENSIONS = {
        'doc',
        'docx',
        'xls',
        'xlsx',
        'ppt',
        'pptx',
        'pdf',
        'jpeg',
        'bmp',
        'gif',
        'png',
        'tiff',
    }

    VALID_OPERATORS = {
        'user',
        'operator',
    }

    def __init__(self, auth_ctx: AuthCtx) -> None:
        self._auth_ctx = auth_ctx

    @property
    def device_id(self):
        return self._auth_ctx.device_id

    def capabilities(self, mode):
        """
        Get device print capabilities.
        """
        method = 'GET'
        path = f'/api/1/printing/printers/{self.device_id}/capability/{mode}'

        return self._auth_ctx.send(method, path)

    def _print_setting(self, settings) -> dict:
        """
        Create a print job.
        """
        method = 'POST'
        path = f'/api/1/printing/printers/{self.device_id}/jobs'

        return self._auth_ctx.send(method, path, settings)

    def _upload_file(self, upload_uri: str, file_path: str, print_mode: str) -> None:
        """
        Upload file to be printed.
        """
        # Get extension from file path.
        extension = pathlib.Path(file_path).suffix.lower()
        if extension[1:] not in self.VALID_EXTENSIONS:
            raise PrinterError(f'{extension} is not a valid printing extension.')

        o = urlparse(upload_uri)
        q_dict = parse_qs(o.query)
        q_dict['File'] = [f'1{extension}']
        path = o._replace(query=urlencode(q_dict)).geturl()

        content_type = 'application/octet-stream'
        if print_mode == 'photo':
            content_type = 'image/jpeg'

        with open(file_path, 'rb') as fp:
            data = fp.read()

        headers = {
            'Content-Type': content_type,
            'Content-Length': str(len(data)),
        }

        method = 'POST'
        self._auth_ctx.send(method, path, data=data, headers=headers)

    def _execute_print(self, job_id):
        """
        Execute print job.
        """
        method = 'POST'
        path = f'/api/1/printing/printers/{self.device_id}/jobs/{job_id}/print'
        self._auth_ctx.send(method, path)

    def print(self, file_path, settings=None) -> str:
        """
        Print file.

        :return: Job ID for print job.
        """
        settings = merge_with_default_settings(settings)
        validate_settings(settings)

        job_data = self._print_setting(settings)
        self._upload_file(job_data['upload_uri'], file_path, settings['print_mode'])
        self._execute_print(job_data['id'])
        return job_data['id']

    def cancel_print(self, job_id, operated_by='user'):
        """
        Cancel print.
        """
        method = 'POST'
        path = f'/api/1/printing/printers/{self.device_id}/jobs/{job_id}/cancel'

        if operated_by not in self.VALID_OPERATORS:
            raise PrinterError(f'Invalid "operated_by" value {operated_by}')

        job_status = self.job_info(job_id).get('status')
        if job_status not in ('pending', 'pending_held'):
            raise PrinterError(f'Can not cancel job with status {job_status}')

        data = {
            'operated_by': operated_by,
        }

        self._auth_ctx.send(method, path, data)

    def job_info(self, job_id):
        """
        Get print job information.
        """
        method = 'GET'
        path = f'/api/1/printing/printers/{self.device_id}/jobs/{job_id}'
        return self._auth_ctx.send(method, path)

    def info(self):
        """
        Get device information.
        """
        method = 'GET'
        path = f'/api/1/printing/printers/{self.device_id}'
        return self._auth_ctx.send(method, path)

    def notification(self, callback_uri, enabled=True):
        """
        Set whether or not to notify of the print job status change.
        """
        method = 'POST'
        path = f'/api/1/printing/printers/{self.device_id}/settings/notifications'

        data = {
            'notification': enabled,
            'callback_uri': callback_uri,
        }

        return self._auth_ctx.send(method, path, data)


class PrinterError(ValueError):
    pass
