from flask import current_app
from papertalk.utils import utils

db = current_app.mongo.db


def update(cls, _id, *E, **doc):
    """
    called to update the reaction
    """
    doc.update(*E)


    return db.articles.update({"_id" : _id},
                              {"$set": doc},
                              safe=True)


def save(cls, title, body, user_id, **doc):
    """
    Called to save or update the reaction.
    """
    doc.update({"title": title,
                "body": body,
                "user": user_id})

    _id = db.articles.insert(doc, safe=True)
    return _id


def lookup(cls, _id=None, title=None, year=None, mult=False):
    """
    lookup a reaction in our db
    """
    if title and year:
        query = {"title": utils.canonicalize(title, year)}
    elif title:
        query = {"title": title}
    elif year:
        query = {"year": year}
    else:
        query = {"_id": _id}

    if mult:
        return db.articles.find(query)
    else:
        return db.articles.find_one(query)
