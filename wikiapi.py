""" A simple restful webservice to provide access to the wiki.db"""
import json
from bottle import Bottle, run, response, static_file, redirect, request
from db.dbfunctions import Wikidb


api = Bottle()

db = Wikidb()

@api.route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='./static')

@api.route('/api/search/<term>')
def search(term):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.search(term))

@api.route('/api/detail/<subject>')
def details(subject):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.detail(subject))


@api.route('/api/put/<subject>/<body>')
def post(subject, body):
    """ This is only a placeholder for a real post method."""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    db.put(subject=subject, body=body)
    return json.dumps(db.detail(subject))

@api.route('/api/tag/<subject>/<tag>')
def tag(subject, tag):
    """Add tag to given subject"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.tag(tag, subject))

@api.route('/api/putjson', method='POST')
def jsonget():
    data = request.json
    print(data)


if __name__ == '__main__':
# Demonstrates the truely awesome awesomplete drawing data right from the search API above.

    @api.route('/search')
    def autocompletesearch():
        return redirect('/static/autocomplete.html')


    db.put('this is an article', 'this is the body of the article.')
    db.put('this is another article', 'this is the body of the article.')
    db.put('this is a third article', 'this is the body of the article.')

    run(api, host='localhost',port=8080, debug=True)

