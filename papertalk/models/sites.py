__author__ = 'karissamckelvey'
from BeautifulSoup import BeautifulSoup
from papertalk.utils import utils, scholar
import article
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

        article = article.Article()
        article["source_url"] = url
        return cls._scrape(soup, article)

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None):
        """
        Retrieve articles from search text, title, author, and/or year
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

        article.save()
        return article

class Mendeley(Site):

    @classmethod
    def _scrape(cls, soup, article):
        ##TODO
        pass

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None):
        ##TODO
        pass


class SSRN(Site):

    @classmethod
    def _scrape(cls, soup, article):
        ##TODO
        pass

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None):
        pass

class IEEE(Site):

    @classmethod
    def _scrape(cls, soup, article):
        ##TODO
        pass

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None):
        pass

class ACM(Site):

    @classmethod
    def _scrape(cls, soup, article):
        ##TODO
        pass

    @classmethod
    def search(cls, text=None, title=None, author=None, year=None):
        pass
