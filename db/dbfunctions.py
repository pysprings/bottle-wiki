from db.dbschema import (
    metadata,
    history,
    authors,
    authorship,
    v_firstlast,
    firstlast,
    tags,
    tagmap,
    select,
    insert,
    func
)
from sqlalchemy import create_engine
from db.utils import hashstring, Config, memoized
from datetime import datetime


""" 
Provides an object for handling data operations in the wiki database.
Defaults to sqlite backend but can use a valid PostgreSQL URL if set in config.json.
"""


class Wikidb(object):
    """ A class for handling wiki data. """

    def __init__(self):
        self.config = Config()
        self.db_url = self.config['DATABASE']['db_url']
        self.debug = bool(self.config['DATABASE']['debug'])
        self.engine = create_engine(self.db_url, echo=self.debug)
        self.metadata = metadata
        self.metadata.create_all(self.engine)
        self.conn = self.engine.connect()
        self.is_postgres = self.engine.dialect.name == 'postgresql'
        self.author(email='anonymous')
        self.history_ids = list()

    def sqldo(self, *args, **kwargs):
        """ Alias for conn.execute """
        return self.conn.execute(*args, **kwargs)

    @memoized
    def _auth_by_id(self, author_id):
        stmt = select([authors]).where(authors.c.author_id == author_id)
        return dict(self.sqldo(stmt).first())

    @memoized
    def _auth_by_email(self, email):
        stmt = select([authors]).where(authors.c.email == email)
        result = self.sqldo(stmt).first()
        if email and not result:
            pkey = self.sqldo(insert(authors).values(email=email)).inserted_primary_key[0]
            return {'email':email, 'author_id':pkey}
        else:
            return dict(result)

    def author(self, **kwargs):
        """A method used for handling authors.
           Returns author info if email or id is provided.
           Creates new author if email does not exist.
        """
        if 'email' in kwargs:
            return self._auth_by_email(kwargs['email'].lower())
        elif 'author_id' in kwargs:
            return self._auth_by_id(kwargs['author_id'])
        else:
            return


    def put(self, subject, body, email='anonymous'):
        """
        This function creates or updates an article.
        """
        history_id = hashstring(body)
        author_id = self.author(email=email)['author_id']
        if history_id not in self.history_ids:
            values_dict = {
                'subject': subject.lower(),
                'history_id': history_id,
                'author_id': author_id,
                'timestamp': func.now()
            }
            stmt = insert(history, sqlite_replace=True)
            if self.is_postgres:
                stmt = stmt.on_conflict_do_update(
                    index_elements=['history_id'], set_=dict(body=stmt.excluded.body)
                )
            self.sqldo(stmt.values(body=body, history_id=history_id))
            self.history_ids.append(history_id)

        stmt = insert(authorship, sqlite_replace=True)
        if self.is_postgres:
            stmt = stmt.on_conflict_do_nothing(constraint='subjectimestamp')
        result = self.sqldo(stmt.values(values_dict))

    def detail(self, subject):
        """ 
        Returns detailed info on an article as a dictionary.
        This is the intended way to fetch article text.
        An empty dict is returned if no exact match for subject so you can safely call .get()
        """
        detail_sql = v_firstlast.where(firstlast.c.subject == subject.lower())

        article_text = self.sqldo(detail_sql).first()
        if not article_text:
            return dict()
        else:
            article_dict = dict(article_text)
            article_dict['last_updated_on'] = article_dict['last_updated_on'].isoformat()
            article_dict['created_on'] = article_dict['created_on'].isoformat()
            article_dict['tags'] = self.taglist(subject)
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

    @memoized
    def _tag(self, tag):
        """A method to get the id of a tag."""
        stmt = select([tags]).where(tags.c.tag == tag)
        result = self.sqldo(stmt).first()
        if not result:
            pkey = self.sqldo(insert(tags).values(tag=tag)).inserted_primary_key[0]
            return {'tag':tag, 'tag_id':pkey}
        else:
            return dict(result)

    def tag(self, tag, subject):
        """ Method for adding a tag to an article """
        tag_id = self._tag(tag)['tag_id']
        stmt = insert(tagmap, sqlite_replace=True)
        if self.is_postgres:
            stmt = stmt.on_conflict_do_nothing(constraint='tagsubject')
        self.sqldo(stmt.values(subject=subject, tag_id=tag_id))

    def taglist(self, subject):
        result = self.sqldo(select([tags.c.tag]).\
                    select_from(tagmap.join(tags, tagmap.c.tag_id == tags.c.tag_id)).\
                    where(tagmap.c.subject == subject))
        return [tag[0] for tag in result]
