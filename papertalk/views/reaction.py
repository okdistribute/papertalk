from flask import render_template, request, Blueprint, redirect
from flask_login import current_user
from papertalk.models import reactions, articles
from papertalk.forms import ReactionForm
from papertalk.utils import disqus

reaction_blueprint  = Blueprint("reaction", __name__)

@reaction_blueprint.route('/reaction/<_id>', methods=["GET"])
def reaction(_id):
    context = {}
    context["reaction"] = reactions.lookup(_id=_id)
    context["article"] = articles.lookup(_id=context["reaction"]['article_id'])
    context["disqus"] = disqus.get(current_user, context["article"], reaction=context["reaction"])

    return render_template('reaction.html', **context)


@reaction_blueprint.route('/article/<article_id>/reaction', methods=["GET", "POST"])
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

