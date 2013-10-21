from papertalk import mongo
from papertalk.models.reaction import Reaction

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

        for key, value in attrs.iteritems():
            self[key] = value

    def save(self):
        article = mongo.db.articles.find_one({"title" : self["title"],
                                              "year"  : self["year"]})
        if article:
            print "article exists"
            mongo.db.articles.save(article)
        else:
            print "creating new article"
            self["_id"] = mongo.db.articles.insert(self)

        return self["_id"]

    def as_txt(self):
        # Get items sorted in specified order:
        return '\n'.join(["%s: %s" % (item[0], item[1]) for item in self.iteritems()])

    @classmethod
    def lookup(cls, title=None, year=None):
        """
        lookup an article in our db
        """
        return mongo.db.articles.find_one({"title": title,
                                           "year": year})
