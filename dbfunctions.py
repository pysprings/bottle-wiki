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

def private_get(subject):
    cur.execute("SELECT article_text FROM articles WHERE subject='{subject}'".format(subject=subject))
    article_text = cur.fetchone()[0]
    return article_text

def search_article(subject_text, strict=False):
    """
    Takes a subject_text and optionally strict boolean.BaseException
    Returns a list of tuples containing: subject, body_text_function
    The body text function can be called to return the body text of the article.
    Strict flag makes searches require an exact match.
    """
    if not strict:
        subject_text = '%'+subject_text+'%'
    search_query = """
    SELECT subject 
    FROM articles 
    WHERE LOWER(subject) like '%{subject}%';
    """.format(subject=subject_text.lower())
    cur.execute(search_query)
    results = cur.fetchall()
    result_list = [[a[0], lambda subj=a[0] : private_get(subject=subj)] for a in results]
    return result_list


