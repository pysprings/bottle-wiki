from db.initialize_db import\
    create_engine,\
    metadata,\
    history,\
    authors,\
    select,\
    insert,\
    authorship,\
    v_firstlast,\
    func,\
    default_author_insert
from db.utils import hashstring, Config
from datetime import datetime


""" 
Provides an object for handling data operations in the wiki database.
Defaults to sqlite backend but can use a valid PostgreSQL URL if set in config.json.
"""


class Wikidb(object):
    """ A class for handling wiki data. """

    def __init__(self):
        self.config = Config()
        self.db_url = self.config.getconfig('db_url')
        self.debug = self.config.getconfig('debug')
        self.engine = create_engine(self.db_url, echo=self.debug)
        self.metadata = metadata
        self.metadata.create_all(self.engine)
        self.conn = self.engine.connect()
        self.is_postgres = self.engine.dialect.name == 'postgresql'
        self.sqldo(default_author_insert(self.engine))

    def sqldo(self, *args, **kwargs):
        """ Alias for conn.execut """
        return self.conn.execute(*args, **kwargs)

    def put(self, subject, body, author_email='anonymous'):
        """
        This function creates or updates an article.
        """
        history_id = hashstring(body)
        values_dict = {
            'subject': subject.lower(),
            'history_id': history_id,
            'author_email': author_email.lower(),
            'timestamp': func.now()
        }
        stmt = insert(history, sqlite_replace=True)
        if self.is_postgres:
            stmt = stmt.on_conflict_do_update(
                index_elements=['history_id'], set_=dict(body=stmt.excluded.body)
            )
        self.sqldo(stmt.values(body=body, history_id=history_id))

        stmt = insert(authorship, sqlite_replace=True)
        if self.is_postgres:
            stmt = stmt.on_conflict_do_nothing(
                index_elements=['subject', 'timestamp'])
        result = self.sqldo(stmt.values(values_dict))

    def detail(self, subject):
        """ 
        Returns detailed info on an article as a dictionary.
        This is the intended way to fetch article text.
        An empty dict is returned if no exact match for subject so you can safely call .get()
        """
        detail_sql = v_firstlast.where(authorship.c.subject == subject.lower())

        article_text = self.sqldo(detail_sql).first()
        if not article_text:
            return dict()
        else:
            article_dict = dict(article_text)
            article_dict['last_updated_on'] = article_dict['last_updated_on'].isoformat()
            article_dict['created_on'] = article_dict['created_on'].isoformat()
            return article_dict

    def search(self, subject_text, strict=False):
        """
        Takes a subject_text and optionally strict True/False.
        Returns a list of article subjects which contain subject_text.
        Strict flag makes searches require an exact match instead of contains.
        """
        if not strict:
            subject_text = '%' + subject_text.lower() + '%'
        search_query = select([authorship.c.subject]).\
            where(authorship.c.subject.like(subject_text)).\
            distinct()

        result = self.sqldo(search_query)
        result_list = [dict(a) for a in result]
        result.close()
        return result_list


if __name__ == "__main__":
    from time import sleep

    wikidb = Wikidb()

    wikidb.put(subject='This is a subject', body='this is a body')

    sleep(10)

    wikidb.put(subject='This is a subject', body='this is a body')

    print(wikidb.search('This'))
    print(wikidb.detail('This is a subject'))