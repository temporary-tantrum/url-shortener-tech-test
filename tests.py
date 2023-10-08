"""
    When the tests pass, the test is putatively complete.
"""
import json
import requests

def test_index():
    """
        hello, world
    """
    r = requests.get('http://localhost:8000/', timeout=1)
    assert r.status_code == 200

def test_post():
    """
        Test that shortening a URL returns a 200 response.
    """
    url_to_shorten = "https://www.google.com"

    r = requests.post('http://localhost:8000/url/shorten',
        data=json.dumps({'url': url_to_shorten}), timeout=1)

    print(r.text)
    assert r.status_code == 200

def test_longen_post():
    """
        Test that longening a URL returns a 200 response.
    """
    url_to_longen = "https://www.google.com"

    r = requests.post('http://localhost:8000/url/longen',
        data=json.dumps({'url': url_to_longen}), timeout=1)

    print(r.text)
    assert r.status_code == 200

def test_redirect():
    """
        Test that the response from the redirect endpoint is, in fact, a redirect.
    """
    r = requests.get('http://localhost:8000/r/abc123', timeout=1,
                        allow_redirects=False)
    assert r.status_code == 307
    # test that the location header is set
    assert r.headers['Location'] == "http://localhost:8000"

def test_that_the_redirect_logic_works_the_way_we_expect_it_to():
    """
        When we give the redirect endpoint a shorten command,
            it should return a code that we can use to
            redirect to the original URL.
    """
    url_to_shorten = "https://wwwww.gooble.email"

    r = requests.post('http://localhost:8000/url/shorten',
        data=json.dumps({'url': url_to_shorten}), timeout=1)

    short_url = r.json()['short_url']
    assert short_url is not None

    r = requests.get(short_url, timeout=1, allow_redirects=False)
    assert r.status_code == 307
    assert r.headers['Location'] == url_to_shorten
