from flask import current_app

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
            db.reactions.update({"_id", self["_id"]},
                                {"$set": self},
                                safe=True)
        else:
            print "creating new reaction"
            self["_id"] = db.reactions.insert(self, safe=True)

        return self["_id"]

    @classmethod
    def lookup(cls, query, mult=False):
        """
        lookup a reaction in our db
        """
        if mult:
            docs = current_app.mongo.db.reactions.find(query)
            res = []
            for d in docs:
                reaction = Reaction()
                reaction.update(d)
                res.append(reaction)
        else:
            res = current_app.mongo.db.reactions.find_one(query)

        return res
