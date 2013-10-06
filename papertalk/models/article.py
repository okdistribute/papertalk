from papertalk.utils import utils, scholar
from datetime import datetime
from papertalk import mongo
from papertalk.models.sites import Scholar
import re


class Article(object):
    """
    An article in papertalk.
    Title (str)
    Author (str)
    Publication Name (str)
    Year (dt)
    Num citations (num)
    Full Citation (text)
    url (str)
    """

    def __init__(self):
        self.attrs = {'title':         None,
                      'authors':       None,
                      'source_url':    None,
                      'num_citations': 0,
                      'url_citations': None,
                      'year':          None,
                      'direct_url':    None}


    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key]
        return None

    def __setitem__(self, key, item):
        if key in self.attrs:
            self.attrs[key] = item

    def __delitem__(self, key):
        if key in self.attrs:
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

    @classmethod
    def search(cls, text):
        """
        Parses the article from a given search string.
        This could be a title (most likely); or an author
        """
        siteClass = Scholar

        return siteClass.search(text=text)

    @classmethod
    def from_url(cls, site, url):
        """
        Scrapes the url and returns a new article
        """
        ##TODO right now, it always assumes google scholar. need to check
        ## which site it is and load appropriately
        siteClass = Scholar


        return siteClass.scrape(url)

