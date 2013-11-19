import urllib
from pymongo import MongoClient
from flask import current_app, session
from flask_oauth import OAuth
from flask import url_for, flash, request, redirect
from flask_login import login_user, current_user
from papertalk.views.main import main_blueprint
from papertalk.models import users
import json
import urllib2

def connect_db():
    c = current_app.config
    if 'MONGO_USERNAME' not in c:
        MONGO_URL = "mongodb://%s:%s/%s" % (c['MONGO_HOST'],
                                            c['MONGO_PORT'],
                                            c['MONGO_DBNAME'])
    else:
        MONGO_URL= "mongodb://%s:%s@%s:%s/%s" % (c['MONGO_USERNAME'],
                                                urllib.quote(c['MONGO_PASSWORD']),
                                                c['MONGO_HOST'],
                                                c['MONGO_PORT'],
                                                c['MONGO_DBNAME'])

    conn = MongoClient(host=MONGO_URL,
                       tz_aware=True)

    db = conn[c['MONGO_DBNAME']]
    return db


def init_google():
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
                              consumer_key=current_app.config['GOOGLE_KEY'],
                              consumer_secret=current_app.config['GOOGLE_SECRET']
    )


    @google.tokengetter
    def get_access_token():
        return session.get('access_token')

    @main_blueprint.route('/oauth-authorized')
    @google.authorized_handler
    def oauth_authorized(resp):
        access_token = resp['access_token']
        session['access_token'] = access_token, ''

        next_url = request.args.get('next') or '/'
        if resp is None:
            return redirect(next_url)

        ## get user data
        params = {
            'access_token': resp['access_token'],
            }
        payload = urllib.urlencode(params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo?' + payload

        req = urllib2.Request(url)  # must be GET
        data = json.loads(urllib2.urlopen(req).read())

        email = data.get('email', '')
        username, domain = email.split('@')

        user = users.get(username=username)
        if not user:
            user = users.create(username, email, data['id'], resp['id_token'])

        login_user(user)

        flash('You were signed in as %s' % user['username'])
        return redirect(next_url)


    @main_blueprint.route('/login')
    def login():
        if current_user.is_authenticated():
            return redirect('/')
        callback=url_for('.oauth_authorized', _external=True)
        return google.authorize(callback=callback)

    return google

