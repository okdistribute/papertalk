from flask import render_template, request, Blueprint
from papertalk.utils import utils
from papertalk.models.results import get_known_articles
from papertalk.models.sites import Scholar, Mendeley
from papertalk.models.article import Article


article_blueprint = Blueprint("article", __name__)

@article_blueprint.route('/article/<ObjectId:id>')
def article(id):
    context = {}
    article = Article.lookup({'_id': id})
    context["article"] = article

    return render_template('article.html', **context)


@article_blueprint.route("/article/search", methods=["GET"])
def article_search():
    """
    Parses the article from a given search string.
    This could be a title (most likely); or an author
    """
    text = request.args.get("query")
    print text

    articles = Scholar.search(text)
    #articles += Mendeley.search(text)

    articles = get_known_articles(articles)
    return render_template("results.html",
                           query=text,
                           articles=articles)

@article_blueprint.route('/article/url', methods=["GET"])
def add_article():
    """
    Scrapes the url and returns a new article
    """
    site = request.form.get("site")
    url = request.form.get("url")

    print site
    print url

    article = {
        "scholar" : Scholar.scrape(url),
        "mendeley" : Mendeley.scrape(url)
    }[site]

    return utils.jsonify(article)



