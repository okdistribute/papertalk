from flask import Flask, Blueprint, url_for, g, flash, request, redirect, session
from papertalk import connect_db
from papertalk.models import users
from flask_login import LoginManager, current_user, login_user
from flask_sslify import SSLify
from utils.RedisSession import RedisSessionInterface
import os
from flask_oauthlib.client import OAuth


def init_login(app):
    login_manager = LoginManager()
    login_manager.login_view = 'login.login'
    login_manager.anonymous_user = users.MyAnonymousUser

    @login_manager.user_loader
    def load_user(_id):
        return users.get(_id=_id)

    login_manager.init_app(app)
    login_blueprint = Blueprint("login", __name__)

    oauth = OAuth()
    twitter = oauth.remote_app('twitter',
                               base_url='https://api.twitter.com/1.1/',
                               request_token_url='https://api.twitter.com/oauth/request_token',
                               access_token_url='https://api.twitter.com/oauth/access_token',
                               authorize_url='https://api.twitter.com/oauth/authenticate',
                               app_key='TWITTER'
    )
    oauth.init_app(app)


    @twitter.tokengetter
    def get_access_token(token=None):
        if current_user.is_authenticated():
            token = current_user['token']
            return token['oauth_token'], token['oauth_token_secret']
        else:
            return None


    @login_blueprint.route('/oauth-authorized')
    @twitter.authorized_handler
    def oauth_authorized(resp):
        next_url = request.args.get('next') or '/'
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(next_url)

        token = (
            resp['oauth_token'],
            resp['oauth_token_secret']
        )
        username = resp['screen_name']
        email = username + "@papertalk.org"

        user = users.get(username=username)
        if not user:
            user = users.create(username, email, token)

        login_user(user)

        return redirect(next_url)

    @login_blueprint.route('/login')
    def login():
        if current_user.is_authenticated():
            return redirect('/')

        callback_url = url_for('.oauth_authorized', next=request.args.get('next'))

        #callback_url = callback_url.replace("http://", "https://")
        #print callback_url

        return twitter.authorize(callback=callback_url or request.referrer or None)

    app.register_blueprint(login_blueprint)


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
        app.config.from_object('papertalk.config')
    except:
        app.config.from_object('papertalk.config_sample')
        for key, value in app.config.iteritems():
            app.config[key] = os.environ.get(key)

    app.secret_key = app.config['SECRET_KEY']
    app.config['DEBUG'] = os.environ.get('DEBUG', True)


    # Function to easily find your assets
    # In your template use <link rel=stylesheet href="{{ static('filename') }}">
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename = filename)
    )

    redis_url = os.getenv('REDISTOGO_URL', False)
    if redis_url:
        import redis
        app.session_interface = RedisSessionInterface(redis = redis.from_url(redis_url))

    @app.before_request
    def before_request():
        g.db = connect_db()

    @app.after_request
    def add_header(response):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'public, max-age=600'
        return response

    @app.context_processor
    def inject_user():
        try:
            user = {'current_user': current_user}
            print "found user ", current_user
        except AttributeError:
            user = {'current_user': None}
            print "AttributeError"

        return user

    register_blueprints(app)
    init_login(app)

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
