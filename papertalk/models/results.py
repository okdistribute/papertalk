__author__ = 'karissamckelvey'
from papertalk.models.article import Article


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

