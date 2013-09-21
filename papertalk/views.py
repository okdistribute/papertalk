from flask import render_template, redirect, request
from papertalk import papertalk

MONGOLAB_URI = "mongodb://heroku_app18165804:kreavs2tvgoo57ljvsss1bk8hj@ds045608.mongolab.com:45608/heroku_app18165804"

@papertalk.route('/')
def index():
	return render_template('index.html')

@papertalk.route('/article/<int:id>')
def article(id):
    context = {}
    context["article"] = {'id': id, 'title': "hello" }
    return render_template('article.html', **context)

@papertalk.route('/article/add', methods=["POST"])
def article_add():
    id = request.form["id"]
    title = request.form["title"]
    print(title)

    redirect("/article/{0}".format(id))

