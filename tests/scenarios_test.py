from hypothesis import example, given, strategies as st
from wsgi_intercept import requests_intercept, add_wsgi_intercept
import requests
import bottle
import app

import pytest

"""
Scenarios:
    User visits / and is redirected to /index
    When /<pagename> has no content, a 404 page is displayed with a link to /<pagename>/edit
    /<pagename>/edit has a form for editing the content and changing the name
    User creates a new page
    User modifies a page
    User browses pages
"""
host, port = 'localhost', 80
url = 'http://{0}:{1}/'.format(host, port)

@pytest.fixture
def db(scope='function'):
    app.db = app.Wikidb(':memory:')
    yield

@pytest.fixture
def wsgi():
    requests_intercept.install()
    add_wsgi_intercept(host, port, bottle.default_app)
    yield
    requests_intercept.uninstall()

@example(slug=u'\x80')
@given(slug=st.text())
def test_get(slug, wsgi, db):
    resp = requests.get(url+slug)
    assert resp.ok or resp.status_code == 404

def test_edit(wsgi, db):
    subject = "Test Subject"
    article = 'This is a test article'
    data = {'subject':subject, 'article':article}
    edit_resp = requests.post(url + 'edit', data=data, allow_redirects=False)
    assert edit_resp.ok
    assert edit_resp.headers['Location'] == 'http://localhost/' + subject
    response = requests.get(url + subject.lower())
    assert article in response.text

def test_edit_post(db, monkeypatch):
    class Stub:
        forms = {'subject':"Test", 'article':"This is a test."}
    monkeypatch.setattr(app, 'request', Stub())
    with pytest.raises(bottle.HTTPResponse):
        app.edit()
