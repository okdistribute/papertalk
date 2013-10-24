__author__ = 'karissamckelvey'
from papertalk.models.article import Article

def get_known_articles(articles):
    """
    Return the known articles from an article result query
    """
    res = []
    for article in articles:
        try:
            a = Article.lookup({"title" : article["title"]})
        except:
            a = article

        res.append(a)
    return res