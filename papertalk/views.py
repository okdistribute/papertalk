from flask import render_template
from papertalk import papertalk

@papertalk.route('/')
def index():
	return render_template('index.html')

@papertalk.route('/article/<int:id>')
def article(id):
    context = {}
    context["article"] = {'id': id, 'title': "hello" }
    return render_template('article.html', **context)

