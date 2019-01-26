import logging
from faat.restclient import RestClient

logging.basicConfig(level=logging.DEBUG)

c = RestClient('http://192.168.1.22/api')
print(c.login.post({'username': 'aaron', 'password': 'secret'}))
print(c.patients['/'].get())
