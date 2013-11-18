from flask import Flask, url_for, g
from papertalk import connect_db
from papertalk.models import users
from flask_login import LoginManager, current_user
import os
from flask_sslify import SSLify
from papertalk import init_google


def init_login(app):
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.anonymous_user = users.MyAnonymousUser

    @login_manager.user_loader
    def load_user(_id):
        return users.get(_id=_id)

    login_manager.init_app(app)


def register_blueprints(app):
    from papertalk.views.reaction import reaction_blueprint
    from papertalk.views.main import main_blueprint
    from papertalk.views.article import article_blueprint

    app.register_blueprint(article_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(reaction_blueprint)


def make_app():
    app = Flask(__name__)
    SSLify(app)

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

    @app.before_request
    def before_request():
        g.db = connect_db()
        init_google()

    @app.context_processor
    def inject_user():
        try:
            user = {'current_user': current_user}
            print "found user ", current_user
        except AttributeError:
            user = {'current_user': None}
            print "AttributeError"

        return user

    init_login(app)
    register_blueprints(app)

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
