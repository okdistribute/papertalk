from flask import Flask, render_template, Blueprint, url_for, g, flash, request, redirect, session
from urllib2 import URLError
from papertalk import connect_db
from papertalk.models import users
from flask_login import LoginManager, session, current_user, login_user
import os
from flask_sslify import SSLify
from flask_oauth import OAuth
import json
import urllib2, urllib


def init_login(app):
    login_manager = LoginManager()
    login_manager.login_view = 'login.login'
    login_manager.anonymous_user = users.MyAnonymousUser

    @login_manager.user_loader
    def load_user(_id):
        return users.get(_id=_id)

    login_manager.init_app(app)

    oauth = OAuth()
    google = oauth.remote_app('google',
                              base_url='https://www.google.com/accounts/',
                              authorize_url='https://accounts.google.com/o/oauth2/auth',
                              request_token_url=None,
                              request_token_params={'scope': 'openid email',
                                                    'response_type': 'code'},
                              access_token_url='https://accounts.google.com/o/oauth2/token',
                              access_token_method='POST',
                              access_token_params={'grant_type': 'authorization_code'},
                              consumer_key=app.config['GOOGLE_KEY'],
                              consumer_secret=app.config['GOOGLE_SECRET']
    )

    @google.tokengetter
    def get_access_token():
        return session.get('access_token')

    login_blueprint = Blueprint("login", __name__)
    @login_blueprint.route('/oauth-authorized')
    @google.authorized_handler
    def oauth_authorized(resp):
        access_token = resp['access_token']
        session['access_token'] = access_token, ''

        next_url = request.referrer or request.args.get('next') or '/'
        if resp is None:
            return redirect(next_url)

        ## get user data
        params = {
            'access_token': resp['access_token'],
            }
        payload = urllib.urlencode(params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo?' + payload

        req = urllib2.Request(url)  # must be GET
        try:
            res = urllib2.urlopen(req)
            data = json.loads(res.read())
        except URLError, e:
            if e.code == 401:
                # Unauthorized - bad token
                session.pop('access_token', None)
                return redirect(url_for('login'))

        email = data.get('email', '')
        username, domain = email.split('@')

        user = users.get(username=username)
        if not user:
            user = users.create(username, email, data['id'], resp['id_token'])

        login_user(user)

        return redirect(next_url)

    @login_blueprint.route('/login')
    def login():
        if current_user.is_authenticated():
            return redirect('/')
        callback=url_for('.oauth_authorized', _external=True)
        return google.authorize(callback=callback)

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
    #app.config['DEBUG'] = os.environ.get('DEBUG', True)


    # Function to easily find your assets
    # In your template use <link rel=stylesheet href="{{ static('filename') }}">
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename = filename)
    )

    @app.before_request
    def before_request():
        g.db = connect_db()

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

    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        from logging import FileHandler
        mail_handler = SMTPHandler('127.0.0.1', 
                                   'server-error@papertalk.org', 
                                   ['support@papertalk.org'],
                                   'Papertalk error')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        file_handler = FileHandler('/tmp/papertalk.log')
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

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
