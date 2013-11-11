import urllib
from pymongo import MongoClient
from flask import current_app
from papertalk.config import Config
from flask_oauth import OAuth
from flask_login import current_user

def connect_db():
    c = current_app.config
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

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key= Config.TWITTER_KEY,
    consumer_secret= Config.TWITTER_SECRET
)


@twitter.tokengetter
def get_twitter_token():
    if current_user.is_authenticated():
        return (current_user['token'], current_user['secret'])
    else:
        return None

