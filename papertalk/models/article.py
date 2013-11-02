from flask import current_app

class Article(dict):
    """
    An article in papertalk.
    Title (str)
    Authors (list of str)
    Year (dt)
    Num citations (num)
    Full Citation (text)
    url (str)
    """


    def __init__(self):
        attrs = {'title':        None,
                'authors':       [],
                'source_urls':   [],
                'reactions':     [],
                'direct_url':    None,
                'num_citations': 0,
                'url_citations': None,
                'url_versions':  None,
                'num_versions':  0,
                'outlet':        None,
                'year':          None,
                'url':           None,
                'doi':           None}
        self.update(attrs)


    def save(self):
        db = current_app.mongo.db
        query = {"title" : self["title"], "year": self["year"]}
        article = db.articles.find_one(query, as_class=dict)
        if article:
            self["_id"] = db.articles.save(article)
        else:
            self["_id"] = db.articles.insert(self, safe=True)

        return self["_id"]

    @classmethod
    def lookup(cls, query, mult=False):
        """
        lookup an article in our db
        """
        db = current_app.mongo.db
        if mult:
            return db.articles.find(query)
        else:
            return db.articles.find_one_or_404(query)

    def disambiguate(self, other):
        """
        returns a new article with the two articles merged
        """
        pass