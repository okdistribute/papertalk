__author__ = 'karissamckelvey'
from BeautifulSoup import BeautifulSoup
from papertalk.utils import utils, scholar
from article import Article
from papertalk.utils.mendeley import mendeley_client as mc
import re

class Site(object):
    """
    Scrapes the site and returns an article
    """

    @classmethod
    def _scrape(cls, soup, article):
        """
        function to implement when extending module
        """
        pass

    @classmethod
    def scrape(cls, url):
        html = utils.scrape(url)
        soup = BeautifulSoup(html)

        article = Article()
        article["source_urls"].append(url)
        return cls._scrape(soup, article)

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None):
        """
        Retrieve a list of articles from search text, title, author, and/or year
        """
        pass

class Scholar(Site):

    @classmethod
    def _scrape(cls, soup, article):
        title = soup.find(id="title")
        if title and title.a:
            article["direct_url"] = title.a["href"]
            article["title"] = title.a.string
        else:
            article["title"] = title.string

        authors = soup.find(text=re.compile("Author"))
        if authors and authors.next:
            authors = authors.next.string.split(",")
            article["authors"] = [a.strip() for a in authors]

        year = soup.find(id="pubdate_sec")
        if year and year.contents and year.contents[1]:
            year_string = year.contents[1].string
            article["year"] = int(year_string.split("/")[0])

        citations = soup.find(id="scholar_sec")
        if citations and citations.a:
            article["num_citations"] = [int(c) for c in citations.a.string.split() if c.isdigit()][0]
            article["url_citations"] = citations.a["href"]

        #TODO: get doi

        return article

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None, items=10):
        """
        Returns a list of article(s) that match this search query
        """
        if not author:
            author = ''

        scholarQuerier = scholar.ScholarQuerier(author)
        scholarQuerier.query(text)
        return scholarQuerier.articles

class Mendeley(Site):

    client = mc.create_client()

    @classmethod
    def _parse(cls, documents):
        """
        returns a list of articles after parsing the response
        article := {u'authors': [{u'forename': u'James G',
                       u'surname': u'Thomson'},
                      {u'forename': u'Ronald',
                       u'surname': u'Chan'},
                      {u'forename': u'Roger',
                       u'surname': u'Thilmony'},
                      {u'forename': u'Yuan-Yeu',
                       u'surname': u'Yau'},
                      {u'forename': u'David W',
                       u'surname': u'Ow'}],
                 u'doi': u'10.1186/1472-6750-10-17',
                 u'mendeley_url': u'http://www.mendeley.com/research/phic31-recombination-system-demonstrates-heritable-germinal-transmission-site-specific-excision-arab/',
                 u'publication_outlet': u'BMC Biotechnology',
                 u'title': u'PhiC31 recombination system demonstrates heritable germinal transmission of site-specific excision from the Arabidopsis genome',
                 u'uuid': u'2c18e9f0-ba04-11df-ae07-0024e8453de6',
                 u'year': 2010}

        response :=  [article, article article]
        """
        res = []
        for article in documents:
            a = Article.lookup(title=article["title"], year=article["year"])
            if not a:
                a = Article()

                for author in article['authors']:
                    a["authors"].append("%s %s" % (author['forename'], author['surname']))

            a["doi"] = article['doi']
            a['source_urls'].append(article['mendeley_url'])
            a['title'] = article['title']
            a['year'] = article['year']
            res.append(a)

        return res


    @classmethod
    def search(cls, text=None, title=None, author=None, year=None, items=15):
        results = cls.client.search(text, items=items)
        docs = results["documents"]
        if docs and "Getting Started with Mendeley" in docs[0]["title"]:
            docs = docs[1:]
        return cls._parse(docs)


class SSRN(Site):

    @classmethod
    def _scrape(cls, soup, article):
        ##TODO
        pass

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None, items=10):
        pass
