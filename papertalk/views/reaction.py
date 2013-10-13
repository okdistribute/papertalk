from flask import render_template, request
from papertalk import papertalk, mongo
from papertalk.utils.utils import jsonify

@papertalk.route('/reaction/<int:id>')
def reaction(id):
    context = {}
    context["reaction"] = mongo.db.find_one({"_id" : id})
    return render_template('reaction.html', **context)

@papertalk.route('/reaction/new')
def reaction_author():
    context = {}
    return render_template('reaction_author.html', **context)

