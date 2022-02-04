import base64
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class RestClient:
    def __init__(self, base_url, *, hyphenate=True, headers=None, bearer=None, auth=None):
        if headers is None:
            headers = {}

        if auth:
            username, password = auth
            headers["AUTHORIZATION"] = format_basic_auth(username, password)

        if bearer:
            headers["AUTHORIZATION"] = "Bearer " + bearer

        self._session = create_session()
        self._headers = headers
        self._base_url = base_url.rstrip("/")
        self._hyphenate = hyphenate

    def __getattr__(self, key):
        name = key.replace('_', '-') if self._hyphenate else key
        return ItemProxy(self, [self._base_url, name])

    def __getitem__(self, key):
        return ItemProxy(self, [self._base_url, key])

    def get(self, **kwargs):
        return self._get([self._base_url, ""], params=kwargs)

    def post(self, *args, **kwargs):
        data = args[0] if len(args) == 1 else args
        return self._post([self._base_url, ""], data=data, params=kwargs)

    def put(self, *args, **kwargs):
        data = args[0] if len(args) == 1 else args
        return self._put([self._base_url, ""], data=data, params=kwargs)

    def patch(self, *args, **kwargs):
        data = args[0] if len(args) == 1 else args
        return self._patch([self._base_url, ""], data=data, params=kwargs)

    def _get(self, parts, params=None):
        url = _create_url(parts)
        r = self._session.get(url, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()

    def _post(self, parts, data, params=None):
        url = _create_url(parts)
        r = self._session.post(url, json=data, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()

    def _put(self, parts, data, params=None):
        url = _create_url(parts)
        r = self._session.put(url, json=data, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()

    def _patch(self, parts, data, params=None):
        url = _create_url(parts)
        r = self._session.patch(url, json=data, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()


class ItemProxy:
    def __init__(self, client, parts):
        self._client = client
        self._parts = parts

    def get(self, **kwargs):
        return self._client._get(self._parts, params=kwargs)

    def post(self, *args, **kwargs):
        data = args[0] if len(args) == 1 else args
        return self._client._post(self._parts, data=data, params=kwargs)

    def put(self, *args, **kwargs):
        data = args[0] if len(args) == 1 else args
        return self._client._put(self._parts, data=data, params=kwargs)

    def patch(self, *args, **kwargs):
        data = args[0] if len(args) == 1 else args
        return self._client._patch(self._parts, data=data, params=kwargs)

    def __getattr__(self, key):
        name = key.replace("_", "-") if self._client._hyphenate else key
        return ItemProxy(self._client, self._parts + [name])

    def __getitem__(self, key):
        return ItemProxy(self._client, self._parts + [key])


def create_session():
    session = requests.Session()
    retry = Retry(total=3, read=3, connect=3, backoff_factor=0.3, status_forcelist=(500, 502, 504))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def format_basic_auth(username, password):
    credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return "Basic " + credentials


def _create_url(parts):
    return "/".join(str(p) for p in parts)
