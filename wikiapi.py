""" A simple restful webservice to provide access to the wiki.db"""
import json
from bottle import Bottle, run, response
from dbfunctions import Wikidb


api = Bottle()

db = Wikidb()

@api.route('/search/<term>')
def search(term):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.search(term))

@api.route('/details/<subject>')
def details(subject):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(db.detail(subject))


if __name__ == '__main__':

    db.put('this is an article', 'this is the body of the article.')
    db.put('this is another article', 'this is the body of the article.')
    db.put('this is a third article', 'this is the body of the article.')
    run(api, host='localhost',port=8080)

