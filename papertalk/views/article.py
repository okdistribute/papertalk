from flask import render_template, request, Blueprint
from papertalk.utils import utils
from papertalk.models.results import get_or_insert_articles
from papertalk.models.sites import Scholar, Mendeley
from papertalk.models.article import Article
from papertalk.models.reaction import Reaction
from bson.objectid import ObjectId


article_blueprint = Blueprint("article", __name__)

@article_blueprint.route('/article/<ObjectId:_id>')
def article(_id):
    context = {}
    article = Article.lookup({'_id': _id})
    reactions = Reaction.lookup({"article_id": ObjectId(_id)}, mult=True)
    context["article"] = article
    context["reactions"] = reactions

    return render_template('article.html', **context)


@article_blueprint.route("/article/search", methods=["GET"])
def article_search():
    """
    Parses the article from a given search string.
    This could be a title (most likely); or an author
    """
    text = request.args.get("query")
    print text

    search_results = Mendeley.search(text)
    #search_results += Scholar.search(text)

    articles = get_or_insert_articles(search_results)
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




