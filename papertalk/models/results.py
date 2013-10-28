__author__ = 'karissamckelvey'
from papertalk.models.article import Article

# TODO deprecated; remove?
def get_known_articles(articles):
    """
    Return the known articles from an article result query
    """
    res = []
    for article in articles:
        try:
            a = Article.lookup({"title" : article["title"], "year": article["year"]})
        except:
            a = article

        res.append(a)
    return res

def get_or_insert_articles(search_results):
    res = []
    titles = set()
    for sr in search_results:
        if sr['canonical_title'] in titles:
            print "duplicate title found: "+sr['canonical_title']
            continue
        titles.add(sr['canonical_title'])

        try:
            a = Article.lookup({'canonical_title': sr['canonical_title']})

        except:
            a = Article()
            a.update(sr)
            a.save()

        res.append(a)

    return res

