from flask import render_template, request, Blueprint, redirect, flash, url_for
from flask_login import current_user
from papertalk import utils
from papertalk.utils import disqus
from papertalk.models.sites import Scholar, Mendeley
from papertalk.models import reactions, articles
from papertalk.forms import ArticleForm

article_blueprint = Blueprint("article", __name__)

@article_blueprint.route('/article/view/<_id>')
def view(_id):
    context = {}
    context["article"] = articles.lookup(_id=_id)
    context["reactions"] = reactions.lookup(article_id=_id, mult=True)
    context["disqus"] = disqus.get(current_user, context["article"])

    return render_template('article.html', **context)


@article_blueprint.route("/article/search", methods=["GET"])
def search():
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
def lookup():
    """
    Lookup article by title, or year
    """
    title = request.args.get("title", None)
    year = request.args.get("year", None)

    return utils.jsonify({"article": articles.lookup(title=title, year=year)})


@article_blueprint.route('/article/url', methods=["GET"])
def url():
    """
    Scrapes the url and returns a new article
    """
    site = request.args.get("site")
    url = request.args.get("query")

    if site == "scholar":
        article = Scholar.scrape(url)
    elif site == "mendeley":
        article = Mendeley.scrape(url)
    else:
        article = {"url": url}

    form = ArticleForm(request.form)

    c = {}
    c['form'] = form
    c.update(article)

    return render_template("article_form.html", **c)

@article_blueprint.route('/article/new', methods=["GET", "POST"])
def add():
    """
    Creates a new article
    """
    form = ArticleForm(request.form)

    if request.method == "POST" and form.validate():
        _id = articles.save(url=form.url.data,
                            title=form.title.data,
                            authors=form.authors.data,
                            year=form.year.data)
        return redirect("/article/view/%s" % _id)

    form = ArticleForm(request.form)

    return render_template("article_form.html", form=form)





