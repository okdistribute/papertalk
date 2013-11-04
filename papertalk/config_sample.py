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
