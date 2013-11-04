from papertalk import utils
from bson.objectid import ObjectId
from flask import g

def update(_id, *E, **doc):
    """
    Called to update an article
    """
    doc.update(*E)

    return g.db.articles.update({"_id" : _id},
                                {"$set": doc},
                                safe=True)

def save(**doc):
    """
    Called to save an article.
    """
    canon = utils.canonicalize(doc['title'])
    doc.update({"canon": canon})

    _id = g.db.articles.insert(doc, safe=True)
    return _id


def lookup(_id=None, title=None, year=None,
           query=None, mult=False):
    """
    Lookup an article in our db
    """

    if not query:
        ## build the query
        query = {}
        if _id:
            query["_id"] =  ObjectId(_id)

        elif title:
            query["canon"] = utils.canonicalize(title)
            if year:
                query["year"] = year

    if mult:
        return g.db.articles.find(query)
    else:
        return g.db.articles.find_one(query)

def get_or_insert(articles):
    """
    takes a list of articles and either gets them from the db or
    inserts them as new articles if they exist already

    find articles where title-first author the same, or title-year the same
    """

    res = []

    for a in articles:
        our_article = lookup(title=a['title'],
                             year=a['year'],
                             mult=False)

        if our_article:
            res.append(our_article)
        else:
            save(**a)
            res.append(a)

    return res
