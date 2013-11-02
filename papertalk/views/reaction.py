from flask import render_template, request, Blueprint, current_app, redirect, url_for
from papertalk.utils.utils import jsonify
from papertalk.models.reaction import Reaction
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
        reaction = Reaction()
        reaction['title'] = request.form['title'].strip()
        reaction['body'] = request.form['text']
        reaction['article_id'] = ObjectId(request.form['article_id'])
        _id = reaction.save()
        return jsonify({'id': _id})



