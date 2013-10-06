__author__ = 'karissamckelvey'
import unittest
from papertalk.models.article import Article
from papertalk import mongo

class TestArticle(unittest.TestCase):

    def setUp(self):
        url = "http://scholar.google.com/citations?view_op=view_citation&hl=en&user=RM2tB8EAAAAJ&citation_for_view=RM2tB8EAAAAJ:u5HHmVD_uO8C"
        self.article = Article.from_scholar_url(url)


    def testFromScholarURL(self):
        """
        Should get an article from google scholar
        """
        article = self.article

        self.assertEqual(article.attrs["scholar_id"], "u5HHmVD_uO8C")
        self.assertEqual(article.attrs["title"], "Visualizing Communication on Social Media: Making Big Data Accessible")
        self.assertEqual(article.attrs["direct_url"], "http://arxiv.org/abs/1202.1367")
        self.assertEqual(article.attrs["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])
        self.assertEqual(article.attrs["num_citations"], 6)
        self.assertEqual(article.attrs["year"], 2012)


    def testSaveArticle(self):
        """
        Save the article and retrieve it
        """

        self.article.save()
        article = mongo.db.find({"scholar_id" : self.article.scholar_id})
        self.assertEqual(article["scholar_id"], "u5HHmVD_uO8C")
        self.assertEqual(article["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])

if __name__ == '__main__':
    unittest.main()



