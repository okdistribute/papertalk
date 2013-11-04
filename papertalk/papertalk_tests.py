__author__ = 'karissamckelvey'
from server import make_app
from flask.ext.testing import TestCase
import json

class PapertalkTestCase(TestCase):

    def create_app(self):
        app = make_app()
        app.config['TESTING'] = True
        return app

    def get_article(self):
        title = "Visualizing Communication on Social Media: Making Big Data Accessible"
        res = self.client.get("/article/lookup?title=%s" % title)

        return res.json['article']

