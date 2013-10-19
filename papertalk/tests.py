__author__ = 'karissamckelvey'
import unittest
from papertalk import mongo, papertalk
from papertalk.models.sites import Scholar, Mendeley
from flask import request

class TestArticle(unittest.TestCase):

    def testFromScholarURL(self):
        """
        Should get an article from google scholar
        """
        with papertalk.app_context():
            url = "http://scholar.google.com/citations?view_op=view_citation&hl=en&user=RM2tB8EAAAAJ&citation_for_view=RM2tB8EAAAAJ:u5HHmVD_uO8C"
            article = Scholar.scrape(url)

            self.assertEqual(article["title"], "Visualizing Communication on Social Media: Making Big Data Accessible")
            self.assertEqual(article["direct_url"], "http://arxiv.org/abs/1202.1367")
            self.assertEqual(article["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])
            self.assertEqual(article["num_citations"], 6)
            self.assertEqual(article["year"], 2012)


    def testMendeley(self):
        text = "visualizing communication on social media: making big data accessible"
        with papertalk.app_context():
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
        with papertalk.app_context():
            url = "http://scholar.google.com/citations?view_op=view_citation&hl=en&user=RM2tB8EAAAAJ&citation_for_view=RM2tB8EAAAAJ:u5HHmVD_uO8C"
            article = Scholar.scrape(url)
            article.save()

            article = mongo.db.articles.find_one({"title" : article['title']})
            self.assertEqual(article["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])


if __name__ == '__main__':
    unittest.main()



