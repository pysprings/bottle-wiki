import sqlite3

conn = sqlite3.connect('wiki.db')

cur = conn.cursor()

# Create if not exists Articles table
tablesql = """
CREATE TABLE IF NOT EXISTS articles (
subject varchar PRIMARY KEY
, article_text VARCHAR NOT NULL
, created_on DATETIME DEFAULT CURRENT_TIMESTAMP
, updated_on DATETIME
);
"""

cur.execute(tablesql)
conn.commit()


def create_article(subject, body):
  """
  This function should insert into the table articles, a new article containing the text and subject specified.  
  """
  cur.execute("INSERT INTO articles (subject, article_text) VALUES ('%s','%s')" % (subject,body))
  conn.commit()

  pass

def update_article(subject, article_text):
  """
  Update an article in the database, based on the subject.
  """
  cur = conn.cursor()

  sql = "UPDATE articles SET article_text=%s updated_on=CURRENT_TIMESTAMP WHERE subject=%s" % (article_text, subject)

  cur.execute(sql)
  conn.commit()


def search_article(subject, strict=False):
  """
  This article should return a list of subjects that contain the subject text given.
  Strict should return only exact match
  Case?
  """
  pass

