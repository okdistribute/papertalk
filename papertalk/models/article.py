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
        attrs = {'_id': None,
                 'title':        None,
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
        article = db.articles.find_one({"title" : self["title"], "year"  : self["year"]})
        if article:
            db.articles.save(article)
        else:
            del self["_id"]
            self["_id"] = db.articles.insert(self)

        return self["_id"]

    def as_txt(self):
        # Get items sorted in specified order:
        return '\n'.join(["%s: %s" % (item[0], item[1]) for item in self.iteritems()])

    @classmethod
    def lookup(cls, query):
        """
        lookup an article in our db
        """
        return current_app.mongo.db.articles.find_one_or_404(query)

    def disambiguate(self, other):
        """
        returns a new article with the two articles merged
        """
        pass