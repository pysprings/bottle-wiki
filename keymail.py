"""
A very simple authentication method for bottle.
Impliments a custom filter for bottle that validates email+uuid keys, consumes, and re-issues them.
"""
import uuid
from dbfunctions import init_db


# Create the auth table if it does not exist.
authtable = """
CREATE TABLE IF NOT EXISTS auth (
email varchar PRIMARY KEY
, auth_key VARCHAR NOT NULL
, keepalive DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

cur, conn = init_db(reqtable=authtable)

def authenticate(email, password=None):
    pass

def passwordify(keymail, password):
    pass


def auth_filter(config):
    ''' Validates and consumes a key '''
    regexp = r'.*'

    def to_python(emailkey):
        # Will only return info if the email and key match and the last keepalive was less than 15 minutes ago.
        in_email, in_key = emailkey.split()
        cur.execute("""SELECT * 
                    FROM auth 
                    WHERE email = ? 
                    AND auth_key = ? 
                    AND 1440 * (julianday(datetime('now')) - julianday(keepalive)) < 15"""
                    , (in_email, in_key))
        check = cur.fetchall()
        if check:
            print("It exists!")
            out_email = in_email
            out_key = str(uuid.uuid4())
            cur.execute ("INSERT OR REPLACE INTO auth (email, auth_key) VALUES (?,?)", (out_email, out_key))
            return {'email':out_email, 'next_key':"{} {}".format(out_email, out_key), 'status':'validated'}
        else:
            return {'email':in_email, 'next_key':None, 'status':'failed_validation'}

    def to_url(key):
        return key

    return regexp, to_python, to_url


if __name__ == "__main__":
    from bottle import Bottle, run

    cur.execute("""INSERT OR REPLACE INTO auth (email, auth_key)
                    VALUES (?, ?)""",
                ('somebody@gmail.com', 'd84011a3-9a53-4980-a2f7-c362e879dfc3'))
    conn.commit()

    app = Bottle()
    app.router.add_filter('auth', auth_filter)

    @app.route('/hello')
    def hello():
        return "Hello World!"

    @app.route('/something/<keymail:auth>')
    def isvalid(keymail):
        return """You tried to validate as {email}
This status is: {status}.
Next Keymail is {next_key} .""".format(**keymail)

    print("Try: http://localhost:8080/somebody@gmail.com d84011a3-9a53-4980-a2f7-c362e879dfc3")
    run(app, host='localhost', port=8080)



# to-do
# Logout function to expire token manually
# Password function to consume token and save a password that can be used to get a token without checking email.
# Additional security checks to expire token (browser changed)
# Make expirtion time configurable
# Make seperator configurable
# Make some password system
