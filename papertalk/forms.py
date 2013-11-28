from wtforms import BooleanField, TextField, PasswordField, validators
from flask_wtf import Form


class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


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
    title = TextField('title', [validators.DataRequired()])
    authors = TextField('authors', [validators.DataRequired()])
    year = TextField('year', [validators.DataRequired()])
    url = TextField('url', [validators.DataRequired()])

