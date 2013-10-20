from papertalk import mongo

class Reaction(object):
    """
    A reaction in papertalk.
    Title (str)
    Body (str) [markdown]
    User (str)
    """

    def __init__(self, reaction_id=None):
        self.attrs = {'_id':   None,
                      'title': None,
                      'body':  None,
                      'user':  None}

        if reaction_id:
            self.load(reaction_id)

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, item):
        self.attrs[key] = item

    def __delitem__(self, key):
        del self.attrs[key]

    def link(self):
        return '/reaction/'+str(self.attrs['_id'])

    def _create(self):
        self.attrs["_id"] = mongo.db.reactions.insert(self.attrs)
        return self.attrs["_id"]

    def load(self, reaction_id):
        self.attrs = mongo.db.reactions.find_one(reaction_id)


    def save(self):
        """
        Called to save or update the reaction.
        """
        if self.attrs['_id']:
            reaction = mongo.db.reactions.find_one({"_id" : self["_id"]})

            if reaction:
                print "updating reaction"
                print self.as_txt()
                mongo.db.reactions.save(self.attrs)
            else:
                raise Exception("weird. this reaction must have been deleted before an update.")
        else:
            print "creating new reaction"
            self._create()

        return self.attrs["_id"]

    def as_txt(self):
        # Get items sorted in specified order:
        return '\n'.join(["%s: %s" % (item[0], item[1]) for item in self.attrs.iteritems()])

    def as_json(self):
        return self.attrs