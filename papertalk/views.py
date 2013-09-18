from flask import render_template
from papertalk import papertalk

@papertalk.route('/')
def index():
	return render_template('index.html')
