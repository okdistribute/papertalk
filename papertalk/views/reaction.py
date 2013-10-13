from flask import render_template, request
from papertalk import papertalk, mongo
from papertalk.utils.utils import jsonify
from papertalk.models.reaction import Reaction

@papertalk.route('/reaction/<int:id>')
def reaction(id):
    context = {}
    context["reaction"] = mongo.db.find_one({"_id" : id})
    return render_template('reaction.html', **context)

@papertalk.route('/reaction/new', methods=["GET", "POST"])
def reaction_author():
    if request.method == "GET":
        context = {}
        return render_template('reaction_author.html', **context)
    elif request.method == "POST":
        reaction = Reaction()
        reaction['title'] = request.form['title'].strip()
        reaction['body'] = request.form['text']
        reaction.save()
        return jsonify({'status': 'reaction saved'})



