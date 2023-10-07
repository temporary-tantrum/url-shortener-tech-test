import requests

def test_index():
	r = requests.get('http://localhost:8000/')
	assert r.status_code == 200

#def test_post():
#	r = requests.post('http://localhost:8000/url/shorten')
#	assert r.status_code == 200