import urllib

class Config(object):
    """
    Config for papertalk. Rename to config.py before running server
    """
    DEBUG = True
    TESTING = True
    MONGO_HOST = ''
    MONGO_PORT = 0000
    MONGO_DBNAME = ''
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    MENDELEY_KEY =  ''
    MENDELEY_SECRET = ''

    MONGO_URL = "mongodb://%s:%s@%s:%s/%s" % (MONGO_USERNAME, urllib.quote(MONGO_PASSWORD), MONGO_HOST, MONGO_PORT, MONGO_DBNAME)

