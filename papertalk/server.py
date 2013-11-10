from flask import Flask, url_for, session, g
from papertalk import connect_db
from papertalk.models import users
from flask_login import LoginManager, current_user
import os

def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(_id):
        return users.get(_id)

    # Make current user available on templates
    @app.context_processor
    def inject_user():
        try:
            return {'user': g.user}
        except AttributeError:
            return {'user': None}

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
        app.config.from_object('papertalk.config.Config')
    except:
        app.config.from_object('papertalk.config_sample.Config')
        for key, value in app.config.iteritems():
            app.config[key] = os.environ.get(key)

    app.secret_key = app.config['SECRET_KEY']


    # Function to easily find your assets
    # In your template use <link rel=stylesheet href="{{ static('filename') }}">
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename = filename)
    )

    init_login(app)
    register_blueprints(app)

    from papertalk import twitter
    @twitter.tokengetter
    def get_twitter_token(token=None):
        return session.get('twitter_token')

    @app.before_request
    def before_request():
        g.db = connect_db()
        g.user = current_user

    app.config['DEBUG'] = True
    return app


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4324)
    parser.add_argument('-d', '--debug', action='store_true', default=True)
    parser.add_argument('--no-debug', action='store_false', dest='debug')

    args = parser.parse_args()

    app = make_app()

    app.run(host='0.0.0.0', port=args.port, debug=args.debug)
