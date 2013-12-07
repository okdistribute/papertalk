__author__ = 'karissamckelvey'
import urlparse
from BeautifulSoup import BeautifulSoup
from papertalk import utils
from papertalk.utils import scholar
from papertalk.utils.mendeley import mendeley_client as mc
import re


class Site(object):
    """
    Scrapes the site and returns an article
    """

    @classmethod
    def _scrape(cls, soup):
        """
        function to implement when extending module
        """
        pass

    @classmethod
    def scrape(cls, url):
        html = utils.scrape(url)
        soup = BeautifulSoup(html)
        return cls._scrape(soup)

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None):
        """
        Retrieve a list of articles from search text, title, author, and/or year
        """
        pass



class Scholar(Site):

    # TODO looks like this scrape method is no longer used?
    @classmethod
    def _scrape(cls, soup):
        title = soup.find(id="title")
        article = {}
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
    def search(cls, text=None, title=None, author='', year=None, items=10):
        """
        Returns a list of article(s) that match this search query
        """
        scholarQuerier = scholar.ScholarQuerier(author)
        scholarQuerier.query(text)

        search_results = scholarQuerier.articles
        for sr in search_results:
            sr['search_source'] = 'scholar'

        return search_results

class Mendeley(Site):


    @classmethod
    def _parse_article(cls, a):
        """
        Parses the article
        """
        authors = a['authors']
        if authors:
            a['firstauthor_surname'] = authors[0]['surname']
            a['authors'] = ["%s %s" % (author['forename'], author['surname']) for author in authors]
        a['url'] = a['mendeley_url']
        return a

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
        for a in documents:
            a = cls._parse_article(a)
            res.append(a)

        return res


    @classmethod
    def search(cls, text=None, title=None, author=None, year=None, page=0):
        client = mc.create_client()
        results = client.search(text, page=page+1)
        docs = results["documents"]
        return cls._parse(docs)

    @classmethod
    def details(cls, id, type=None):
        client = mc.create_client()
        results = client.details(id, type=type)
        try:
            article = cls._parse_article(results)
            article[type] = id
            return article
        except:
            return None

    @classmethod
    def _scrape(cls, soup):
        """
        function to implement when extending module
        """
        pass

    @classmethod
    def from_url(cls, url):
        return {"url": url}

class SSRN(Site):

    @classmethod
    def from_url(cls, url):
        parsed = urlparse.urlparse(url)
        params = urlparse.parse_qs(parsed.query)
        id = params.get('abstract_id')
        if not id:
            parsed = url.rsplit('=', 1)
            id = parsed[1]

        return Mendeley.details(id, type='ssrn')

class Arxiv(Site):

    @classmethod
    def from_url(cls, url):
        parsed = url.rsplit('/', 1)
        id = parsed[1]
        return Mendeley.details(id, type='arxiv')

class PubMed(Site):

    @classmethod
    def from_url(cls, url):
        parsed = url.rsplit('/', 1)
        id = parsed[1]
        return Mendeley.details(id, type='pmid')

class PDF(Site):

    @classmethod
    def scrape(cls, url):
        return ''
