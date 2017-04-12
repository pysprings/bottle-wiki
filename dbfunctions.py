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
  This function should update the article in table articles with subject specified. 
  It should set the article_text to the text specified.  
  An error should be returned if the subject does not exist.
  """
  pass

def search_article(subject, strict=False):
  """
  This article should return a list of subjects that contain the subject text given.
  Strict should return only exact match
  Case?
  """
  pass
