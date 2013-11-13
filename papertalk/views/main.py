from flask import render_template, Blueprint, url_for, g, flash, request, redirect, session
from flask_login import login_required, login_user, logout_user, current_user
from papertalk.models import users
from papertalk import google
import json
import urllib2, urllib

main_blueprint  = Blueprint("main", __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/about')
def about():
	return render_template('about.html')

@main_blueprint.route('/get-involved')
def get_involved():
	return render_template('get-involved.html')

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

    email = data['email']

    user = users.get(username=email)
    if not user:
        user = users.create(email, email, data['id'], resp['id_token'])

    login_user(user)

    flash('You were signed in as %s' % user['username'])
    return redirect(next_url)

@main_blueprint.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect('/')
    callback=url_for('.oauth_authorized', _external=True)
    return google.authorize(callback=callback)

@main_blueprint.route("/settings")
@login_required
def settings():
    pass

@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
