import requests
import pytest
import bottle
import wikiapi
from wsgi_intercept import requests_intercept, add_wsgi_intercept


host, port = 'localhost', 8080
url = 'http://{0}:{1}/'.format(host, port)

@pytest.fixture
def wsgi():
    requests_intercept.install()
    add_wsgi_intercept(host, port, bottle.default_app)
    yield
    requests_intercept.uninstall()

def test_json(wsgi):
    payload = {
        "subject": "more"
        , "body": "this"
        , "email": "giblesnot@gmail.com"
        , "tags":["books"
                , "articles"
                , "english"]
    }
    urlbase = 'http://{host}:{port}'.format(host=host, port=port)
    r = requests.post(urlbase + '/api/putjson', json=payload)

    response_json = requests.get(urlbase + '/api/detail/more')
    details = response_json.json()

    assert payload['tags'] == details['tags']
    assert payload['body'] == details['body']

def test_put(wsgi):
    payload = {
        "subject": "more"
        , "body": "this"
    }
    urlbase = 'http://{host}:{port}'.format(host=host, port=port)
    r = requests.post(urlbase + '/api/put/{subject}/{body}'.format(**payload))

    response_json = requests.get(urlbase + '/api/detail/more')
    details = response_json.json()

    assert payload['body'] == details['body']
    assert payload['subject'].lower() == details['subject'].lower()
    