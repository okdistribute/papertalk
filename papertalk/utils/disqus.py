import base64
import hashlib
import hmac
import simplejson
import time
from flask import current_app

class Disqus(object):
    """
    Handles the transfer of disqus information to the templates
    """

    def __init__(self, user, identifer, title):
        self.sso_script = get_sso_script(user)
        self.identifier = identifer
        self.title = title

def get(user, article, reaction=None):
    """
    Returns an object to be consumed by disqus comment js
    Article is required.
    """
    title = "Comments for this "
    if reaction:
        identifier = "%s/%s" % (article["_id"], reaction["_id"])
        title += "reaction:"
    else:
        identifier = article["_id"]
        title += "article:"

    return Disqus(user, identifier, title)

def get_sso_script(user):
    # create a JSON packet of our data attributes
    data = simplejson.dumps({
        'id': str(user.get('_id', None)),
        'username': user.get('username', None),
        'email': user.get('email', None)
    })
    # encode the data to base64
    message = base64.b64encode(data)
    # generate a timestamp for signing the message
    timestamp = int(time.time())
    # generate our hmac signature
    sig = hmac.HMAC(current_app.config['DISQUS_SECRET'], '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()

    # return a script tag to insert the sso message
    return """<script type="text/javascript">
    var disqus_config = function() {
        this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";
    }
    </script>""" % dict(
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=current_app.config['DISQUS_PUBLIC'],
    )
