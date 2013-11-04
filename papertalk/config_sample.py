import urllib

class Config(object):
    """
    Config for papertalk. Rename to config.py before running server
    """
    DEBUG = True
    TESTING = True
    MONGO_HOST='localhost'
    MONGO_PORT=27018
    MONGO_DBNAME='papertalk'
    MONGO_USERNAME='travis'
    MONGO_PASSWORD='test'
    MONGO_URL = "mongodb://%s:%s@%s:%s/%s" % (MONGO_USERNAME, urllib.quote(MONGO_PASSWORD), MONGO_HOST, MONGO_PORT, MONGO_DBNAME)

