from flask import g
from flask_login import AnonymousUserMixin

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

class MyAnonymousUser(AnonymousUserMixin, dict):
    def __init__(self):
        self['_id'] = None
        self['username'] = None

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

def get(_id=None, username=None):
    """
    Gets a user by id
    """
    q = {}

    if _id:
        q["_id"] = _id
    elif username:
        q["username"] = username
    else:
        return None

    return g.db.users.find_one(q, as_class=User)

def create(username, email, google_id, token, **doc):
    """
    Creates a new user
    """
    doc.update({'username': username,
                '_username': username.lower(),
                'email': email,
                'google_id': google_id,
                'token': token,
                'is_active':True
               })

    _id = g.db.users.insert(doc, safe=True)
    user = User({"_id": _id})

    return user

