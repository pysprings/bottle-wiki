from db.dbfunctions import Wikidb

w = Wikidb()

print(w.author(email='bob6'))

print(w.author(author_id=1))

w.put(subject='thing #2', body='body text here', email='giblesnot@gmail.com')


w.tag('magic', 'thing #2')
w.tag('maps', 'thing #2')

print(w.detail(subject='thing #2'))

print(w.search(''))


import requests

payload = {
    "subject": "more"
    , "body": "this"
    , "email": "giblesnot@gmail.com"
    , "tags":["books"
              , "articles"
              , "english"]
}

r = requests.post('http://localhost:8080/api/putjson', json=payload)
r.status_code

r= requests.get('http://localhost:8080/api/detail/more')
details = r.json()

for item in payload:
    assert item in details