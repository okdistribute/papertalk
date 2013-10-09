from papertalk import mongo

class Article(object):
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
        self.attrs = {'title':         None,
                      'authors':       [],
                      'source_url':    None,
                      'num_citations': 0,
                      'url_citations': None,
                      'url_versions':  None,
                      'num_versions':  0,
                      'year':          None,
                      'url':           None}


    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, item):
        self.attrs[key] = item

    def __delitem__(self, key):
        del self.attrs[key]

    def save(self):
        article = mongo.db.articles.find_one({"title" : self["title"],
                                              "year" : self["year"]})
        if article:
            print "article exists"
            article_id = article["_id"]
        else:
            print "creating new article"
            article_id = mongo.db.articles.insert(self.attrs)

        return article_id

    def as_txt(self):
        # Get items sorted in specified order:
        return '\n'.join(["%s: %s" % (item[0], item[1]) for item in self.attrs.iteritems()])

    def as_csv(self, header=False, sep='|'):
        # Get keys sorted in specified order:
        keys = [pair[0] for pair in \
                    sorted([(key, val[2]) for key, val in self.attrs.items()],
                           key=lambda pair: pair[1])]
        res = []
        if header:
            res.append(sep.join(keys))
        res.append(sep.join([unicode(self.attrs[key][0]) for key in keys]))
        return '\n'.join(res)

    def as_json(self):
        return self.attrs