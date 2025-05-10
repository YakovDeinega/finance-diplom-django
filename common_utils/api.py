from urllib.parse import urljoin

import requests


class BaseAPIService:

    @property
    def host(self):
        raise NotImplementedError

    @property
    def token(self):
        raise NotImplementedError

    @property
    def api_path(self):
        raise NotImplementedError

    def _get_headers(self):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def _request(self, method, endpoint, **kwargs):
        url = urljoin(self.host, f'{self.api_path}/{endpoint}')
        headers = self._get_headers()

        if kwargs.get('headers'):
            headers.update(kwargs['headers'])
            del kwargs['headers']

        response = requests.request(method, url, headers=headers, **kwargs)
        return response

    @classmethod
    def get(cls, endpoint, **kwargs):
        return cls()._request('GET', endpoint, **kwargs)

    @classmethod
    def post(cls, endpoint, **kwargs):
        return cls()._request('POST', endpoint, **kwargs)

    @classmethod
    def put(cls, endpoint, **kwargs):
        return cls()._request('PUT', endpoint, **kwargs)

    @classmethod
    def delete(cls, endpoint, **kwargs):
        return cls()._request('DELETE', endpoint, **kwargs)
