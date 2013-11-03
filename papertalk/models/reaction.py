"""
A reaction in papertalk.
Title (str)
Body (str) [markdown]
User (str)
"""
from bson.objectid import ObjectId
from papertalk.models import db


def update(_id, *E, **doc):
    """
    Called to update the reaction
    """
    doc.update(*E)

    return db.reactions.update({"_id" : _id},
                                   {"$set": doc},
                                    safe=True)


def save(title, body, user_id, article_id, **doc):
    """
    Called to save or update the reaction.
    """
    doc.update({"title": title,
                "body": body,
                "user": user_id,
                "article_id": article_id})


    _id = db.reactions.insert(doc, safe=True)
    return _id


def lookup(_id=None, article_id=None, user_id=None, mult=False):
    """
    Lookup a reaction in our db
    """

    if article_id:
        query = {"article_id": ObjectId(article_id)}
    elif user_id:
        query = {"user_id": user_id}
    else:
        query = {"_id": _id}
    if mult:
        return db.reactions.find(query)
    else:
        return db.reactions.find_one(query)
