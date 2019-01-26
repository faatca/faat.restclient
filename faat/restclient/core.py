import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class RestClient:
    def __init__(self, base_url, headers=None):
        self._session = create_session()
        self._headers = headers
        self._base_url = base_url.rstrip('/')
        self._translations = {'_': '-'}

    def __getattr__(self, key):
        return ItemProxy(self, [self._base_url, key])

    def __getitem__(self, key):
        return ItemProxy(self, [self._base_url, key])

    def get(self, **kwargs):
        return self._client._get([], params=kwargs)

    def post(self, data, **kwargs):
        return self._client._post([], data=data, params=kwargs)

    def put(self, data, **kwargs):
        return self._client._put([], data=data, params=kwargs)

    def _get(self, parts, params=None):
        url = translate_url(parts, self._translations)
        r = self._session.get(url, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()

    def _post(self, parts, data, params=None):
        url = translate_url(parts, self._translations)
        r = self._session.post(url, json=data, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()

    def _put(self, parts, data, params=None):
        url = translate_url(parts, self._translations)
        r = self._session.put(url, json=data, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()


def translate_url(parts, translations):
    def translate(word):
        if word == '/':
            return ''
        return ''.join(translations.get(c, c) for c in word)

    return '/'.join(translate(str(p)) for p in parts)


class ItemProxy:
    def __init__(self, client, parts):
        self._client = client
        self._parts = parts

    def get(self, **kwargs):
        return self._client._get(self._parts, params=kwargs)

    def post(self, data, **kwargs):
        return self._client._post(self._parts, data=data, params=kwargs)

    def put(self, data, **kwargs):
        return self._client._put(self._parts, data=data, params=kwargs)

    def __getattr__(self, key):
        return ItemProxy(self._client, self._parts + [key])

    def __getitem__(self, key):
        return ItemProxy(self._client, self._parts + [key])


def create_session():
    session = requests.Session()
    retry = Retry(total=3, read=3, connect=3, backoff_factor=0.3, status_forcelist=(500, 502, 504))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
