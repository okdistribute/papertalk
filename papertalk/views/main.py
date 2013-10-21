from flask import render_template
from papertalk import papertalk

@papertalk.route('/')
def index():
	return render_template('index.html')

@papertalk.route('/about')
def about():
	return render_template('about.html')

@papertalk.route('/get-involved')
def get_involved():
	return render_template('get-involved.html')


