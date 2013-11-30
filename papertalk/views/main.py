from flask import render_template, Blueprint, request, redirect, session
from flask_login import login_required, logout_user

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

@main_blueprint.route("/settings")
@login_required
def settings():
    pass

@main_blueprint.route("/logout")
@login_required
def logout():
    session.pop('twitter_oauth', None)
    logout_user()
    return redirect(request.referrer)
