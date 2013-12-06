import urllib, urllib2
import re
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug import Response
import pytz


def scrape(url):
    """
    Scrapes a url and returns the html using the proper User Agent
    """
    UA = 'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9'
    urllib.quote(url.encode('utf-8'))
    req = urllib2.Request(url=url,
                          headers={'User-Agent': UA})
    hdl = urllib2.urlopen(req)
    html = hdl.read()
    return html

def utcnow():
    now = datetime.utcnow()
    return now.replace(tzinfo=pytz.utc)


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId"""
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')


def canonicalize(title):
    """
    canonicalizes an article title
    """

    def normalize(s):
        """
        normalizes given string for the canonicalization
        """
        if not isinstance(s, basestring):
            return ''

        res = s.lower().strip() ## lowercase and remove outer spaced
        res = re.sub("\s", '', res) ## remove spaces
        res = re.sub("""["`'.&]""", '', res) ## normalize quotes
        res = re.sub("""[&apos;]""", '', res) ## weird unicode found on mendeley articles

        return res

    canon = normalize(title)

    return canon

