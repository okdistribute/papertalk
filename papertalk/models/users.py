from papertalk import utils
from werkzeug.security import generate_password_hash
from flask import g
from flask_login import login_user, current_user, login_required, logout_user

class User(dict):

    def __repr__(self):
        return 'User(%r)' % (self['username'])

    def get_id(self):
        return str(self['_id'])

    def is_active(self):
        return bool(not self.get('_inactive', False))

    def is_anonymous(self):
        if self['_id']:
            return False
        return True

    def is_authenticated(self):
        if self['_id']:
            return True
        return False

def update(user, *E, **doc):
    """
    Updates a user
    """
    doc.update(*E)

    return g.db.users.update({"_id" : user['_id']},
                             {"$set": doc},
                            safe=True)

def save(**doc):
    """
    Called to save a user.
    """
    _id = g.db.users.insert(doc, safe=True)
    return _id

def get(_id):
    """
    Gets a user by id
    """
    return g.db.users.find_one(_id=_id)

def create(username, **doc):
    """
    Creates a new user
    """
    doc.update({'username':username,
                '_username':username.lower(),
                'is_active':True
               })

    _id = db.users.insert(doc, safe=True)
    user = User({"_id": _id})
    return user


