from flask import Flask, url_for
from flask.ext.pymongo import PyMongo
from views import *
import os

papertalk = Flask(__name__)
try:
    papertalk.config.from_object('config.Config')
except:
    papertalk.config["MONGO_HOST"] = os.environ.get("MONGO_HOST")
    papertalk.config["MONGO_PORT"] = os.environ.get("MONGO_PORT")
    papertalk.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
    papertalk.config["MONGO_USERNAME"] = os.environ.get("MONGO_USERNAME")
    papertalk.config["MONGO_PASSWORD"] = os.environ.get("MONGO_PASSWORD")

mongo = PyMongo(papertalk)

# Determines the destination of the build. Only usefull if you're using Frozen-Flask
papertalk.config['FREEZER_DESTINATION'] = os.path.dirname(os.path.abspath(__file__))+'/../build'

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
papertalk.jinja_env.globals['static'] = (
	lambda filename: url_for('static', filename = filename)
)

from papertalk.views import article, main, reaction
