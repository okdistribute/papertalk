from flask import render_template, request, Blueprint
from flask_login import current_user
from papertalk import utils
from papertalk.utils import disqus
from papertalk.models.sites import Scholar, Mendeley
from papertalk.models import reactions, articles

article_blueprint = Blueprint("article", __name__)

@article_blueprint.route('/article/view/<_id>')
def article(_id):
    context = {}
    context["article"] = articles.lookup(_id=_id)
    context["reactions"] = reactions.lookup(article_id=_id, mult=True)
    context["disqus"] = disqus.get(current_user, context["article"])

    return render_template('article.html', **context)


@article_blueprint.route("/article/search", methods=["GET"])
def article_search():
    """
    Parses the article from a given search string.
    This could be a title (most likely); or an author
    """
    text = request.args.get("query")
    search_results = Mendeley.search(text)

    return render_template("results.html",
                           query=text,
                           articles=articles.get_or_insert(search_results))


@article_blueprint.route("/article/lookup", methods=["GET"])
def article_lookup():
    """
    Lookup article by title, or year
    """
    title = request.args.get("title", None)
    year = request.args.get("year", None)

    return utils.jsonify({"article": articles.lookup(title=title, year=year)})


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


