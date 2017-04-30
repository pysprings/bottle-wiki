import sqlite3
from hashlib import md5

def hash(text):
    return md5(text.encode()).hexdigest()

class Wikidb(object):
    """ A class for handling wiki data. """

    def __init__(self, db_path='wiki.db'):
        with open('initialize.sql', 'r') as sql:
            self.tablesql = sql.read().split(';')
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        for command in self.tablesql:
            self.cur.execute(command)
        self.conn.commit()

    def put(self, subject, body, author_email='anonymous'):
        """
        This function creates or updates an article.
        """
        history_id = hash(str(subject+body))
        self.cur.execute("""INSERT OR REPLACE INTO history (body, history_id)
        VALUES (?,?)""", (body, history_id))
        self.cur.execute("""INSERT OR REPLACE INTO articles (subject, history_id)
        VALUES (?,?)""", (subject.lower(), history_id))
        self.cur.execute("""INSERT INTO authorship(article_subject, author_email, history_id)
        VALUES(?, ?, ?)""", (subject.lower(), author_email.lower(), history_id))
        self.conn.commit()

    def detail(self, subject):
        """ Needs docstring """
        sql = """
        SELECT subject
        , created_on
        , creator_email
        , last_updated_on
        , updator_email
        , body
        FROM v_first_last
        WHERE subject = ?;
        """
        self.cur.execute(sql, [subject])
        article_text = self.cur.fetchone()[0]
        return article_text

    def search(self, subject_text, strict=False):
        """
        Takes a subject_text and optionally strict True/False.
        Returns a list of article subjects which contain subject_text.
        Strict flag makes searches require an exact match instead of contains.
        """
        if not strict:
            subject_text = '%'+subject_text.lower()+'%'
        search_query = """
        SELECT subject
        FROM articles
        WHERE subject like ?;
        """
        self.cur.execute(search_query, [subject_text])
        return list(self.cur.fetchall())
