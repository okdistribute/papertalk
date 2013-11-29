"""
A reaction in papertalk.
Title (str)
Body (str) [markdown]
User (str)
"""
from bson.objectid import ObjectId
from flask import g
import articles

def update(_id, *E, **doc):
    """
    Called to update the reaction
    """
    doc.update(*E)

    return g.db.reactions.update({"_id" : ObjectId(_id)},
                                   {"$set": doc},
                                    safe=True)


def save(title=None, body=None, article_id=None, username=None, **doc):
    """
    Called to save the reaction.
    """
    doc.update({"title": title,
                "body": body,
                "username": username,
                "article_id": ObjectId(article_id)})

    _id = g.db.reactions.insert(doc, safe=True)


    articles.add_reaction(article_id, _id)

    return _id


def lookup(_id=None, article_id=None, user_id=None, mult=False):
    """
    Lookup a reaction in our g.db
    """
    query = {}

    if article_id:
        query["article_id"] = ObjectId(article_id)
    if user_id:
        query["user_id"] = ObjectId(user_id)
    if _id:
        query["_id"] = ObjectId(_id)

    if mult:
        return g.db.reactions.find(query)
    else:
        return g.db.reactions.find_one(query)
