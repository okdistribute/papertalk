from flask import Flask, url_for
from flask.ext.pymongo import PyMongo
import os

def register_blueprints(app):
    from papertalk.views.reaction import reaction_blueprint
    from papertalk.views.main import main_blueprint
    from papertalk.views.article import article_blueprint

    app.register_blueprint(article_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(reaction_blueprint)

def make_app():
    app = Flask(__name__)
    try:
        app.config.from_object('config.Config')
    except:
        app.config.from_object('config_sample.Config')
        for key, value in app.config.iteritems():
            app.config[key] = os.environ.get(key)
    app.mongo = PyMongo(app)

    # Determines the destination of the build. Only usefull if you're using Frozen-Flask
    app.config['FREEZER_DESTINATION'] = os.path.dirname(os.path.abspath(__file__))+'/../build'
    # Function to easily find your assets
    # In your template use <link rel=stylesheet href="{{ static('filename') }}">
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename = filename)
    )
    register_blueprints(app)

    return app


if __name__ == "__main__":
    app = make_app()
    app.run(port=4324, debug=True)
