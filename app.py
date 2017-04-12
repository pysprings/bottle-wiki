from bottle import request, route, run, template, post, get, TEMPLATE_PATH
from marshmallow import Schema, fields

TEMPLATE_PATH.append('templates')


class ArticleSchema(Schema):
  body = fields.Str()

class Article():
  def __init__(self, body):
    self.body = body


@route('/')
def index():
  return template('index.html')

@route('/edit')
def edit_view():
  return template('edit.html')

@post('/edit')
def edit():
  # import pdb;pdb.set_trace()

  article = Article(request.forms.get('article'))
  schema = ArticleSchema()
  data, errors = schema.dump(article)
  return data['body']

if __name__ == '__main__':
  run(host='localhost', port=8080, debug=True)
