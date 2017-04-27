import dbfunctions

def test_create_article():
    dbfunctions.init_db(':memory:')
    dbfunctions.create_article("Test Subject", "Test Body")
