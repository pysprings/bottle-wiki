import bottle
import webtest
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

@pytest.fixture
def db(scope='function'):
    app.dbfunctions.init_db(':memory:')
    yield
    app.dbfunctions.init_db()

@pytest.fixture
def testapp():
    return webtest.TestApp(bottle.default_app())

def test_index(testapp):
    response = testapp.get('/')
    assert response.status == '200 OK'

def test_edit(db, testapp):
    article = 'This is a test article'
    testapp.post('/edit', params={'subject':'Test Subject', 'article':article})
    response = testapp.get('/test')
    assert article in response.body.decode('UTF-8')

def test_edit_squeeze(db, monkeypatch):
    class Stub:
        forms = {'subject':"Test", 'article':"This is a test."}
    monkeypatch.setattr(app, 'request', Stub())
    app.edit()
