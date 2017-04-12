import sqlite3

conn = sqlite3.connect('wiki.db')

cur = conn.cursor()

tablesql = """
CREATE TABLE IF NOT EXISTS articles (
subject varchar PRIMARY KEY
, article_text VARCHAR NOT NULL
, created_on DATETIME DEFAULT CURRENT_TIMESTAMP
, updated_on DATETIME
);
"""

cur.execute(tablesql)

cur.execute("INSERT INTO articles (subject, article_text) VALUES ('this','article body')")

cur.execute('SELECT * FROM articles;')
thingy = cur.fetchall()

for thing in thingy:
    print(thing)

conn.commit()
conn.close()
