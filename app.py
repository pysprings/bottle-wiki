from bottle import request, route, run, template, post, get, TEMPLATE_PATH
from marshmallow import Schema, fields
import dbfunctions

TEMPLATE_PATH.append('templates')


class ArticleSchema(Schema):
  body = fields.Str()
  subject = fields.Str()

class Article():
  def __init__(self, body, subject):
    self.body = body
    self.subject = subject

@route('/')
def index():
  return template('index.html')

@route('/<subject>')
def view_article(subject):

  db_result = dbfunctions.search_article(subject, False)

  if db_result:
    _, get_function = db_result[0]
    body = get_function()

    return body + ' ' + subject
  else:
    return 'Not found.'



@route('/edit')
def edit_view():
  return template('edit.html')

@post('/edit')
def edit():

  # article = Article()

  body = request.forms.get('article')
  subject = request.forms.get('subject')

  article = Article(body = body, subject = subject)

  schema = ArticleSchema()
  data, errors = schema.dump(article)
  # import pdb;pdb.set_trace()
  dbfunctions.create_article(subject, body)

  return data['body']

if __name__ == '__main__':
  run(host='localhost', port=8080, reloader=True)
