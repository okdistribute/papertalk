"""
A reaction in papertalk.
Title (str)
Body (str) [markdown]
User (str)
"""
from flask import current_app
from bson.objectid import ObjectId

db = current_app.mongo.db

def update(cls, _id, *E, **doc):
    """
    called to update the reaction
    """
    doc.update(*E)

    return cls.db.reactions.update({"_id" : _id},
                                   {"$set": doc},
                                    safe=True)


def save(cls, title, body, user_id, article_id, **doc):
    """
    Called to save the reaction.
    """
    doc.update({"title": title,
                "body": body,
                "user": user_id,
                "article_id": article_id})


    _id = cls.db.reactions.insert(doc, safe=True)
    return _id


def lookup(cls, _id=None, article_id=None, user_id=None, mult=False):
    """
    lookup a reaction in our db
    """

    if article_id:
        query = {"article_id": ObjectId(article_id)}
    elif user_id:
        query = {"user_id": user_id}
    else:
        query = {"_id": _id}
    if mult:
        return cls.db.reactions.find(query)
    else:
        return cls.db.reactions.find_one(query)
