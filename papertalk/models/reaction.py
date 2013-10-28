from flask import current_app
from bson.objectid import ObjectId

class Reaction(dict):
    """
    A reaction in papertalk.
    Title (str)
    Body (str) [markdown]
    User (str)
    """

    def __init__(self):
        attrs = ({'title': None,
                 'body':  None,
                 'user':  None,
                 'article_id': None})

        for key, value in attrs.iteritems():
            self[key] = value        

    def save(self):
        """
        Called to save or update the reaction.
        """
        db = current_app.mongo.db
        if '_id' in self:
            reaction = db.reactions.find_one({"_id" : self["_id"]})

            if reaction:
                print "updating reaction"
                print self.as_txt()
                db.reactions.save(self.attrs)
            else:
                raise Exception("weird. this reaction must have been deleted before an update.")
        else:
            print "creating new reaction"
            self["_id"] = db.reactions.insert(self)

        return self["_id"]

    @classmethod
    def lookup(cls, query):
        """
        lookup a reaction in our db
        """
        return current_app.mongo.db.reactions.find_one_or_404(query)

    @classmethod
    def for_article(cls, article_id):
        """
        lookup reactions for an article
        """
        docs = current_app.mongo.db.reactions.find({"article_id": ObjectId(article_id)})
        res = []
        for d in docs:
            reaction = Reaction()
            reaction.update(d)
            res.append(reaction)

        return res

    def link(self):
        return '/reaction/'+str(self['_id'])

    def as_txt(self):
        return '\n'.join(["%s: %s" % (item[0], item[1]) for item in self.attrs.iteritems()])

    def as_json(self):
        return self.attrs