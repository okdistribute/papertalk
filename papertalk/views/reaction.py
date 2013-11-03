from flask import render_template, request, Blueprint, current_app, redirect, url_for
from papertalk.utils.utils import jsonify
from papertalk.models import reaction
from bson.objectid import ObjectId

reaction_blueprint  = Blueprint("reaction", __name__)

@reaction_blueprint.route('/reaction/<ObjectId:id>', methods=["GET"])
def reaction(id):
    context = {}
    db = current_app.mongo.db
    reaction = db.reactions.find_one_or_404({"_id" : id})
    article = db.articles.find_one_or_404({"_id" : reaction['article_id']})
    context["reaction"] = reaction
    context["article"] = article
    return render_template('reaction.html', **context)

@reaction_blueprint.route('/reaction/new', methods=["GET", "POST"])
def reaction_author():
    if request.method == "GET":
        context = {}
        context['article_id'] = request.args.get('article')
        return render_template('reaction_author.html', **context)

    elif request.method == "POST":
        title = request.form['title'].strip()
        body = request.form['text']
        article_id = request.form['article_id']
        reaction.save(title=title,
                      body=body,
                      article_id=article_id)

        return redirect("/article/%s" % reaction["article_id"])


