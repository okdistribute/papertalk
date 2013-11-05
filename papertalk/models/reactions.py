"""
A reaction in papertalk.
Title (str)
Body (str) [markdown]
User (str)
"""
from bson.objectid import ObjectId
from flask import g

def update(_id, *E, **doc):
    """
    Called to update the reaction
    """
    doc.update(*E)

    return g.db.reactions.update({"_id" : ObjectId(_id)},
                                   {"$set": doc},
                                    safe=True)


def save(title=None, body=None, article_id=None, **doc):
    """
    Called to save or update the reaction.
    """
    doc.update({"title": title,
                "body": body,
                "article_id": ObjectId(article_id)})

    _id = g.db.reactions.insert(doc, safe=True)
    print _id

    return _id


def lookup(_id=None, article_id=None, user_id=None, mult=False):
    """
    Lookup a reaction in our g.db
    """

    if article_id:
        query = {"article_id": ObjectId(article_id)}
    elif user_id:
        query = {"user_id": ObjectId(user_id)}
    else:
        query = {"_id": ObjectId(_id)}

    if mult:
        return g.db.reactions.find(query)
    else:
        return g.db.reactions.find_one(query)
