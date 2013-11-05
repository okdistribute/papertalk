from flask import render_template, request, Blueprint, redirect
from papertalk.models import reactions, articles

reaction_blueprint  = Blueprint("reaction", __name__)

@reaction_blueprint.route('/reaction/<id>', methods=["GET"])
def reaction(id):
    context = {}
    r = reactions.lookup(_id=id)
    context["reaction"] = r
    context["article"] = articles.lookup(_id=r['article_id'])
    return render_template('reaction.html', **context)


@reaction_blueprint.route('/reaction/new', methods=["GET", "POST"])
def reaction_author():
    if request.method == "GET":
        context = {}
        context['article_id'] = request.args.get('article')
        return render_template('reaction_author.html', **context)

    elif request.method == "POST":
        print "HELLO"
        title = request.form['title'].strip()
        body = request.form['body']
        article_id = request.form['article_id']
        reactions.save(title=title,
                       body=body,
                       article_id=article_id)

        return redirect("/article/%s" % article_id)


