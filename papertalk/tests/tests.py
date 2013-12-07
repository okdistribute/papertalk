__author__ = 'karissamckelvey'
import unittest
import json
from papertalk.models.sites import Scholar, Mendeley
from papertalk.tests import PapertalkTestCase

class TestArticle(PapertalkTestCase):

    def testMendeley(self):
        text = "visualizing communication on social media: making big data accessible"
        articles = Mendeley.search(text)
        self.assertGreater(len(articles), 0)
        for article in articles:
            if article['title'] == "Visualizing Communication on Social Media: Making Big Data Accessible":
                self.assertEqual(article["authors"], ["Karissa McKelvey", "Alex Rudnick", "Michael D Conover", "Filippo Menczer"])
                self.assertEqual(article["year"], 2012)


    def testSaveArticle(self):
        """
        Save the article and retrieve it
        """
        text = "visualizing communication on social media: making big data accessible"
        res = self.client.get("/article/search?query=%s" % text)
        self.assert200(res)
        self.assertIn('visualizing communication', res.data)

    def testViewArticle(self):
        """
        View the article
        """
        article = self.get_article()
        res = self.client.get("/article/view/%s" % article["_id"])
        self.assert200(res)

class TestReaction(PapertalkTestCase):

    def testReactionSave(self):
        """
        Should be able to create a reaction
        """
        article = self.get_article()

        res = self.client.get("/article/view/%s" % article["_id"])
        self.assert200(res)

        token = self.csrf_token(res)

        res = self.client.post("/article/%s/reaction" % article["_id"],
                data=dict(
                  csrf_token=token,
                  title="this is a reaction title",
                  text="reaction text here"
                ))
        self.assert200(res)


        res = self.client.get('/reaction/%s' % json.loads(res.data)["id"])
        self.assert200(res)

        self.assertIn("this is a reaction title", res.data)


if __name__ == '__main__':
    unittest.main()

