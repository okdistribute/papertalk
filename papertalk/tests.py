__author__ = 'karissamckelvey'
import unittest
from papertalk import make_app
from papertalk.models.sites import Scholar, Mendeley
from flask.ext.testing import TestCase
from flask.ext.pymongo import PyMongo

class TestArticle(TestCase):

    def create_app(self):
        app, self.mongo = make_app()
        app.config['TESTING'] = True
        return app

    def testFromScholarURL(self):
        """
        Should get an article from google scholar
        """
        url = "http://scholar.google.com/citations?view_op=view_citation&hl=en&user=RM2tB8EAAAAJ&citation_for_view=RM2tB8EAAAAJ:u5HHmVD_uO8C"
        article = Scholar.scrape(url)

        self.assertEqual(article["title"], "Visualizing Communication on Social Media: Making Big Data Accessible")
        self.assertEqual(article["direct_url"], "http://arxiv.org/abs/1202.1367")
        self.assertEqual(article["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])
        self.assertEqual(article["num_citations"], 6)
        self.assertEqual(article["year"], 2012)


    def testMendeley(self):
        text = "visualizing communication on social media: making big data accessible"
        articles = Mendeley.search(text)
        self.assertGreater(len(articles), 0)
        article = articles[0]
        self.assertEqual(article["title"], "Visualizing Communication on Social Media: Making Big Data Accessible")
        self.assertEqual(article["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])
        self.assertEqual(article["year"], 2012)

    def testSaveArticle(self):
        """
        Save the article and retrieve it
        """
        url = "http://scholar.google.com/citations?view_op=view_citation&hl=en&user=RM2tB8EAAAAJ&citation_for_view=RM2tB8EAAAAJ:u5HHmVD_uO8C"
        article = Scholar.scrape(url)
        article.save()

        article = self.mongo.db.articles.find_one({"title" : article['title']})
        self.assertEqual(article["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])


    def testViewArticle(self):
        """
        View the article
        """
        title = "Visualizing Communication on Social Media: Making Big Data Accessible"
        article = self.mongo.db.articles.find_one({"title" : title})

        assert article
        
        #res = self.client.get(url)
        #self.assert200(res)

        #res = self.client.get("/article/{0}".format("notaproperid"))
        #self.assert404(res)

if __name__ == '__main__':
    unittest.main()

