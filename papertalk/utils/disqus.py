import base64
import hashlib
import hmac
import simplejson
import time
from flask import current_app

def get_sso_script(user):
    # create a JSON packet of our data attributes
    data = simplejson.dumps({
        'id': user['_id'],
        'username': user['screen_name'],
        'email': user.get('email', None),
        'url': user.get('url', None)
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
