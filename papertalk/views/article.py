from flask import render_template, request
from papertalk.models.article import Article
from papertalk import papertalk, mongo
from papertalk.utils.utils import jsonify

@papertalk.route('/article/<int:id>')
def article(id):
    context = {}
    context["article"] = mongo.db.find_one({"_id" : id})
    return render_template('article.html', **context)

@papertalk.route("/article/search")
def article_search():
    """
    Search the database, then mendeley, then scholar
    """
    q = request.form.get("text")


@papertalk.route('/article/url', methods=["POST"])
def add_article():
    site = request.form.get("site")
    print site
    url = request.form.get("url")
    article = Article.from_url(url)

    return jsonify(article.attrs)

