import dbfunctions

def test_create_article():
    db = dbfunctions.Wikidb(':memory:')
    db.put("Test Subject", "Test Body")
