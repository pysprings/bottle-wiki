import re
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    select,
    and_
)
from sqlalchemy.sql import func
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.dialects.postgresql import insert
from db.utils import hashstring


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

history = Table(
    'history'
    , metadata
    , Column('history_id', String(32), primary_key=True, nullable=False, default=hash_body)
    , Column('body', String(100), nullable=False)
)

authors = Table(
    'authors'
    , metadata
    , Column('author_id', Integer(), primary_key=True)
    , Column('email', String(100), nullable=False, unique=True)
)

authorship = Table(
    'authorship'
    , metadata
    , Column('authorship_id', Integer(), primary_key=True)
    , Column('subject', String(100), nullable=False)
    , Column('history_id', String(32), ForeignKey('history.history_id'))
    , Column('author_id', Integer(), ForeignKey('authors.author_id'))
    , Column('timestamp', DateTime, server_default=func.now())
    , UniqueConstraint('subject', 'timestamp', name='subjectimestamp')
)

tags = Table(
    'tags'
    , metadata
    , Column('tag_id', Integer(), primary_key=True, nullable=False)
    , Column('tag', String(100), unique=True)
)

tagmap = Table(
    'tagmap'
    , metadata
    , Column('tagmap_id', Integer(), primary_key=True, nullable=False)
    , Column('tag_id', Integer(), ForeignKey('tags.tag_id'), nullable=False)
    , Column('subject', String(100), nullable=False)
    , UniqueConstraint('tag_id', 'subject', name='tagsubject')
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
, creator.c.author_id.label("creator_id")
, firstlast.c.last_updated_on
, updator.c.author_id.label("updator_id")
, history.c.body]

v_firstlast = select(column_list).select_from(firstlast.\
join(creator, and_(firstlast.c.subject == creator.c.subject,
firstlast.c.created_on == creator.c.timestamp)).\
join(updator, and_(firstlast.c.subject == updator.c.subject,
firstlast.c.last_updated_on == updator.c.timestamp)).\
join(history, history.c.history_id == updator.c.history_id)
)


if __name__ == "__main__":
    import sys
    sys.path.append("..")
    print(firstlast.compile())