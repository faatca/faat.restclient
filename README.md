faat.restclient package
=======================

This package provides a simple way to access typical JSON REST APIs.

This package won't do everything for every API.
It's a small wrapper around the superb requests package and makes accessing many APIs very convenient.


```python
from faat.restclient import RestClient

client = RestClient("http://192.168.1.22:3000/api")
client.login.post({"username": "aaron", "password": "secret"})
patients = client.patients["/"].get(active=True)["patients"]

for p in patients:
    print(client.patients[p["id"]].get())
    exams = client.patients[p["id"]].exams["/"].get(criteria="test")["exams"]
    print(exams)
    for e in exams:
        print("overview", e)
        details = client.patients[p["id"]].exams[e["id"]].get()
        print("detail", details)
```

It support several shortcuts for common authorization needs.
For example, basic authentication is managed with the `auth` argument.

```pycon
>>> api = RestClient("https://httpbin.org", auth=("username", "password"))
>>> api.basic_auth["username"]["password"].get()
{'authenticated': True, 'user': 'username'}
```

It's easy to provide a bearer token with the `bearer` argument.

```pycon
>>> api = RestClient("https://httpbin.org", bearer="1234")
>>> api.bearer.get()
{'authenticated': True, 'token': '1234'}
```

Finally, with the headers argument, you can specify any needed header.

```python
api = RestClient(
    "http://192.168.1.22:3000/api",
    headers={"X-VAULT-TOKEN": 'd16e34aa5329d1bdcc6b1d0540bcda914307c9978d4b0d5e5ff0dafe34606eb5'},
)
```

Many APIs prefer hyphens to underscores in their resource names.
By default, the RestClient replaces python underscores in attribute names when converting attribute names to a path.
For example, the identifer `api.active_connections["test_name"].get()` maps to the url path `/active-connections/test_name`.
Disable this behaviour with the hyphenate argument when this doesn't make sense.

```python
api = RestClient(url, hyphenate=False)
```
