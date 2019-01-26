faat.restclient package
=======================

This package provides a simple way to access typical JSON REST APIs.

This package won't do everything for every API.
It's a small wrapper around the superb requests package and makes accessing many APIs very convenient.


.. sourcecode:: python

	import faat.restclient

	client = faat.restclient.RestClient('http://192.168.1.22:3000/api')
	client.login.post({'username': 'aaron', 'password': 'secret'})
	patients = client.patients['/'].get(active=True)['patients']

	for p in patients:
	    print(client.patients[p["id"]].get())
	    exams = client.patients[p["id"]].exams["/"].get(criteria="test")['exams']
	    print(exams)
	    for e in exams:
	        print("overview", e)
	        details = client.patients[p["id"]].exams[e["id"]].get()
	        print("detail", details)
