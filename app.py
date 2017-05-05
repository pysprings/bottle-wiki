from bottle import request, route, run, template, post, TEMPLATE_PATH, abort, redirect
from marshmallow import Schema, fields
from dbfunctions import Wikidb

TEMPLATE_PATH.append('templates')
DB_PATH = './wiki.db'


class ArticleSchema(Schema):
    body = fields.Str()
    subject = fields.Str()


class Article():
    def __init__(self, body, subject):
        self.body = body
        self.subject = subject


@route('/')
def index():
    return template('index.html', subject='PySprings Wiki', body='Under Construction')


@route('/<subject>')
def view_article(subject):
    db_result = db.detail(subject)
    if db_result:
        return template('index.html',  subject=db_result.get('subject',''), body=db_result.get('body',''))
    else:
        return abort(404, 'Not found.')


@route('/<subject>/edit')
def edit_view(subject):
    db_result = db.detail(subject)
    return template('edit.html', subject=subject, body=db_result.get('body',''))


@post('/edit')
def edit():
    body = request.forms.get('article')
    subject = request.forms.get('subject')

    article = Article(body=body, subject=subject)

    schema = ArticleSchema()
    data, errors = schema.dump(article)
    db.put(subject, body)
    return redirect('/' + subject)


if __name__ == '__main__':
    db = Wikidb(db_path=DB_PATH)
    run(host='localhost', port=8080, debug=True)
