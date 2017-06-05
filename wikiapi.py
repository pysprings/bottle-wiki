""" A simple restful webservice to provide access to the wiki.db"""
import json
from bottle import run, response, static_file, redirect, request, route
from db.dbfunctions import Wikidb

db = Wikidb()

@route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='./static')

@route('/api/search/<term>')
def search(term):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.search(term))

@route('/api/detail/<subject>')
def details(subject):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.detail(subject))


@route('/api/put/<subject>/<body>')
def post(subject, body):
    """ This is only a placeholder for a real post method."""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    db.put(subject=subject, body=body)
    return json.dumps(db.detail(subject))

@route('/api/tag/<subject>/<tag>')
def addtag(subject, tag):
    """Add tag to given subject"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.tag(tag, subject))

@route('/api/putjson', method='POST')
def jsonget():
    data = dict(request.json)
    db.put(subject=data.get('subject'), body=data.get('body'), email=data.get('email', 'anonymous'))
    if 'tags' in data and 'subject' in data:
        print(data['tags'])
        subject = data.get('subject')
        for t in data['tags']:
            db.tag(t, subject)


if __name__ == '__main__':
# Demonstrates the truely awesome awesomplete drawing data right from the search API above.

    @route('/search')
    def autocompletesearch():
        return redirect('/static/autocomplete.html')


    db.put('this is an article', 'this is the body of the article.')
    db.put('this is another article', 'this is the body of the article.')
    db.put('this is a third article', 'this is the body of the article.')

    run(host='localhost',port=8080, debug=True)

