from papertalk import models, config
from pymongo import MongoClient

def connect_db():
    c = config.Config

    host = c.MONGO_URL
    db_name = c.MONGO_DBNAME

    conn = MongoClient(host=host,
                       tz_aware=True)

    db = conn[db_name]
    return db

