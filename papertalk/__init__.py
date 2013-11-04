from pymongo import MongoClient
from flask import current_app

def connect_db():
    c = config.Config

    host = current_app.config.MONGO_URL
    db_name = current_app.config.MONGO_DBNAME

    conn = MongoClient(host=host,
                       tz_aware=True)

    db = conn[db_name]
    return db

