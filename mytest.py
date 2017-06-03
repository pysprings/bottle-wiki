from db.dbfunctions import Wikidb

w = Wikidb()

print(w.author(email='bob6'))

print(w.author(author_id=1))

w.put(subject='thing #2', body='body text here', email='giblesnot@gmail.com')

print(w.detail(subject='thing #2'))

w.tag('magic', 'thing #2')
w.tag('maps', 'thing #2')

print(w.taglist('thing #2'))