from flask import render_template, Blueprint, url_for, g, session, flash, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
from papertalk.models import users
from papertalk import google

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

    user = users.get(screen_name=resp['email'])
    if not user:
        user = users.create(resp['email'], resp['client_id'], resp['client_secret'])

    login_user(user)
    users.update(user, email=resp['email'])

    flash('You were signed in as %s' % user['email'])
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
