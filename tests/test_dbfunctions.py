import dbfunctions
import pytest
from hypothesis import given, strategies as st

@pytest.fixture
def db(scope='function'):
    db = dbfunctions.Wikidb(':memory:')
    yield db
    db = None

def test_create_article():
    db = dbfunctions.Wikidb(':memory:')
    db.put("Test Subject", "Test Body")

@given(subject=st.text(), body=st.text())
def test_db_scaletest(subject, body, db):
    """ Aim for 10,000 articles """
    for i in range(0,9999):
        db.put(subject, body)