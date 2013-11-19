import urllib
from pymongo import MongoClient
from flask import current_app, session
from papertalk.config import Config
from flask_oauth import OAuth

def connect_db():
    c = current_app.config
    if 'MONGO_USERNAME' not in c:
        MONGO_URL = "mongodb://%s:%s/%s" % (c['MONGO_HOST'],
                                            c['MONGO_PORT'],
                                            c['MONGO_DBNAME'])
    else:
        MONGO_URL= "mongodb://%s:%s@%s:%s/%s" % (c['MONGO_USERNAME'],
                                                urllib.quote(c['MONGO_PASSWORD']),
                                                c['MONGO_HOST'],
                                                c['MONGO_PORT'],
                                                c['MONGO_DBNAME'])

    conn = MongoClient(host=MONGO_URL,
                       tz_aware=True)

    db = conn[c['MONGO_DBNAME']]
    return db

oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'openid email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key= Config.GOOGLE_KEY,
                          consumer_secret= Config.GOOGLE_SECRET
)

@google.tokengetter
def get_access_token():
    return session.get('access_token')

