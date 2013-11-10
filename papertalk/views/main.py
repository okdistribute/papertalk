from flask import render_template, Blueprint, url_for, g, session, flash, request
from forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, logout_user
from models import users
from papertalk import twitter

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
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    print resp

    user = users.create(resp['screen_name'])
    login_user(user)

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

@main_blueprint.route('/login')
def login():
    return twitter.authorize(callback=url_for('.oauth_authorized',
        next=request.args.get('next') or request.referrer or None))


@main_blueprint.route("/settings")
@login_required
def settings():
    pass

@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)
