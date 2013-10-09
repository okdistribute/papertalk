from flask import render_template, request
from papertalk import papertalk, mongo
from papertalk.utils.utils import jsonify
from papertalk.models.sites import Scholar

@papertalk.route('/article/<int:id>')
def article(id):
    context = {}
    context["article"] = mongo.db.find_one({"_id" : id})
    return render_template('article.html', **context)

@papertalk.route("/article/search")
def article_search():
    """
    Parses the article from a given search string.
    This could be a title (most likely); or an author
    """
    text = request.args.get("query", "")
    print text

    ##TODO right now, it always assumes google scholar. need to cycle through sites
    articles = Scholar.search(text=text)
    print articles

    return jsonify({"articles" : [a.as_json() for a in articles]})


@papertalk.route('/article/url', methods=["POST"])
def add_article():
    """
    Scrapes the url and returns a new article
    """
    site = request.form.get("site")
    url = request.form.get("url")

    print site
    print url

    ##TODO right now, it always assumes google scholar. need to check which site it is and load appropriately
    article = Scholar.scrape(url)

    return jsonify(article.attrs)


