import re
from sqlalchemy import create_engine, Table, Column, String, MetaData, ForeignKey, DateTime, select, insert, and_
from sqlalchemy.sql import func
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.dialects.postgresql import insert
from utils import hashstring


metadata = MetaData()

@compiles(Insert, 'sqlite')
def compile_replace(insert, compiler, **kw):

    stmt = compiler.sql_compiler.visit_insert(insert)
    if not insert.kwargs['sqlite_replace']:
        return stmt
    else:
        return re.sub(r'^INSERT', 'INSERT OR REPLACE', stmt)

Insert.argument_for("sqlite", "replace", None)

hash_body = lambda context:hashstring(context.current_parameters['body'])

history = Table('history', metadata
, Column('history_id', String(32), primary_key=True, nullable=False, default=hash_body)
, Column('body', String(100), nullable=False)
)

authors = Table('authors', metadata
, Column('email', String(100), primary_key=True, nullable=False)
)

authorship = Table('authorship', metadata
, Column('subject', String(100), primary_key=True)
, Column('history_id', String(32), ForeignKey('history.history_id'))
, Column('author_email', String(100), ForeignKey('authors.email'))
, Column('timestamp', DateTime, primary_key=True, server_default=func.now())
)

firstlast = select([authorship.c.subject,
func.min(authorship.c.timestamp).label("created_on"),
func.max(authorship.c.timestamp).label("last_updated_on")]).\
select_from(authorship).group_by(authorship.c.subject).\
correlate(None).\
alias()

creator = authorship.alias()
updator = authorship.alias()

column_list = [firstlast.c.subject.label("subject")
, firstlast.c.created_on
, creator.c.author_email.label("creator_email")
, firstlast.c.last_updated_on
, updator.c.author_email.label("updator_email")
, history.c.body]

v_firstlast = select(column_list).select_from(firstlast.\
join(creator, and_(firstlast.c.subject == creator.c.subject,
    firstlast.c.created_on == creator.c.timestamp)).\
join(updator, and_(firstlast.c.subject == updator.c.subject,
    firstlast.c.last_updated_on == updator.c.timestamp)).\
join(history, history.c.history_id == updator.c.history_id)
)


def default_author_insert(engine):
    insert_default = insert(authors, sqlite_replace=True) 
    if engine.dialect.name == 'postgresql':
        insert_default = insert_default.on_conflict_do_nothing(
                index_elements=['email'])
    return insert_default.values(email='anonymous')