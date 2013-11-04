import urllib
from pymongo import MongoClient
from flask import current_app

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

