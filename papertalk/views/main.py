from flask import render_template, Blueprint, url_for, g, session, flash, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
from papertalk.models import users
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
    next_url = request.args.get('next') or '/'
    if resp is None:
        return redirect(next_url)

    user = users.get(screen_name=resp['screen_name'])
    if not user:
        user = users.create(resp['screen_name'], resp['oauth_token'], resp['oauth_token_secret'])

    login_user(user)
    data = twitter.get('account/verify_credentials.json').data
    users.update(user, avatar=data['profile_image_url'], url=data['url'], email='unique@uniquewa.unei')

    flash('You were signed in as %s' % user['screen_name'])
    return redirect(next_url)

@main_blueprint.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect('/')
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
    return redirect('/')
