CREATE TABLE IF NOT EXISTS history (
history_id VARCHAR PRIMARY KEY
, body VARCHAR
);

CREATE TABLE IF NOT EXISTS authors (
email VARCHAR PRIMARY KEY
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS authorship (
article_subject VARCHAR
, history_id VARCHAR
, author_email VARCHAR
, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
, PRIMARY KEY (article_subject, timestamp)
, FOREIGN KEY(author_email) REFERENCES authors(email)
, FOREIGN KEY(history_id) REFERENCES history(history_id)
) WITHOUT ROWID;

INSERT OR REPLACE INTO authors(email) VALUES ('anonymous');

DROP VIEW IF EXISTS v_first_last;

CREATE VIEW v_first_last AS
SELECT firstlast.article_subject subject
    , firstlast.created_on
    , creator.author_email creator_email
    , firstlast.last_updated_on
    , updator.author_email updator_email
    , history.body
FROM ( 
    SELECT article_subject, MIN(timestamp) created_on, MAX(timestamp) last_updated_on
    FROM authorship
    GROUP BY article_subject
    ) AS firstlast
LEFT JOIN authorship AS creator ON creator.article_subject = firstlast.article_subject 
    AND creator.timestamp = firstlast.created_on
LEFT JOIN authorship AS updator ON updator.article_subject = firstlast.article_subject 
    AND updator.timestamp = firstlast.last_updated_on
LEFT JOIN history ON updator.history_id = history.history_id;
