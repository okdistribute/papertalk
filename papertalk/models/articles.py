from papertalk import utils
from papertalk.models.sites import Mendeley
from bson.objectid import ObjectId
from flask import g


def get_details(article):
    deets = Mendeley.details(article['uuid'])

    del deets['authors']
    update(article, **deets)

    return lookup(article['_id'])


def add_reaction(_id, reaction_id):
    """
    Add a reaction to an article
    """

    article = lookup(_id=_id)
    r = article.get('reactions', [])
    r.append(reaction_id)
    update(article, reactions=r)


def update(article, *E, **doc):
    """
    Called to update an article
    """
    doc.update(*E)

    return g.db.articles.update({"_id" : article['_id']},
                                {"$set": doc},
                                safe=True)

def save(url=None, canon=None, title=None, authors=None, year=None, **doc):
    """
    Called to save an article.
    """
    if type(authors) == str:
        authors = [a.strip() for a in authors.split(',')]

    doc.update({"canon": canon,
                "title": title,
                "authors": authors,
                "year": year})

    _id = g.db.articles.insert(doc, safe=True)
    return _id


def lookup(_id=None, canon=None, year=None,
           query=None, mult=False):
    """
    Lookup an article in our db
    """

    if not query:
        ## build the query
        query = {}
        if _id:
            query["_id"] =  ObjectId(_id)

        elif canon:
            query["canon"] = canon
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

    res = {}

    i = 0
    for a in articles:
        a['i'] = i
        a['canon'] = utils.canonicalize(a['title'])
        our_article = lookup(canon=a['canon'],
                             mult=False)

        if our_article:
            _id = our_article['_id']
            res[_id] = our_article
        else:
            _id = save(**a)
            res[_id] = lookup(_id=_id)

        i += 1

    l = res.values()
    return sorted(l, key=lambda x: x['i'])


