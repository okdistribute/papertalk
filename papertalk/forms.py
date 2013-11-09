from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class ReactionForm(Form):
    """
    Form that creates a reaction.
    """
    title = TextField('title', [validators.Required()])
    body = TextField('body', [validators.Required()])

class ArticleForm(Form):
    """
    Form that creates an article.
    """
    title = TextField('title', [validators.Required()])
    authors = TextField('authors', [validators.Required()])
    year = TextField('year', [validators.Required()])

