from flask import current_app
from papertalk.utils import utils

class Article(object):
    """
    {'_id': None,
     'title':        '',
    'authors':       [],
    'source_urls':   [],
    'reactions':     [],
    'direct_url':    '',
    'num_citations': 0,
    'url_citations': '',
    'url_versions':  '',
    'num_versions':  0,
    'outlet':        '',
    'year':          None,
    'url':           '',
    'doi':           ''}
    """
    db = current_app.mongo.db

    @classmethod
    def update(cls, _id, *E, **doc):
        """
        called to update the reaction
        """
        doc.update(*E)


        return cls.db.articles.update({"_id" : _id},
                                      {"$set": doc},
                                      safe=True)


    @classmethod
    def save(cls, title, body, user_id, **doc):
        """
        Called to save or update the reaction.
        """
        doc.update({"title": title,
                    "body": body,
                    "user": user_id})

        _id = cls.db.articles.insert(doc, safe=True)
        return _id

    @classmethod
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
            return cls.db.articles.find(query)
        else:
            return cls.db.articles.find_one(query)
