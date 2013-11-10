from flask import render_template, request, Blueprint, redirect
from papertalk.models import reactions, articles
from papertalk.forms import ReactionForm
from papertalk.utils import disqus

reaction_blueprint  = Blueprint("reaction", __name__)

@reaction_blueprint.route('/reaction/<id>', methods=["GET"])
def reaction(id):
    context = {}
    reaction = reactions.lookup(_id=id)
    context["reaction"] = reaction
    context["article"] = articles.lookup(_id=reaction['article_id'])
    context["disqus_sso_script"] = disqus.get_sso_script(user)
    return render_template('reaction.html', **context)


@reaction_blueprint.route('/article/<article_id>/reaction/new', methods=["GET", "POST"])
def reaction_author(article_id):
    form = ReactionForm(request.form)

    if request.method == "POST" and form.validate():
        reactions.save(title=form.title.data,
                       body=form.body.data,
                       article_id=article_id)
        return redirect("/article/view/%s" % article_id)

    context = {}
    context['article_id'] = article_id
    context['form'] = form

    return render_template('reaction_author.html', **context)

