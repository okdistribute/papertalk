from papertalk import mongo

class Reaction(object):
    """
    A reaction in papertalk.
    Title (str)
    Body (str) [markdown]
    User (str)
    """

    def __init__(self):
        self.attrs = {'id':            None,
                      'title':         None,
                      'body':          None,
                      'user':          None}


    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, item):
        self.attrs[key] = item

    def __delitem__(self, key):
        del self.attrs[key]

    def save(self):
        if self['id']:
            reaction = mongo.db.reactions.find_one({"_id" : self["id"]})

            if reaction:
                print "reaction exists"
                reaction_id = reaction["_id"]
            else:
                print "reaction id not found"
                # FIXME
                reaction_id = None

        else:
            print "creating new reaction"
            reaction_id = mongo.db.reactions.insert(self.attrs)

        return reaction_id

    def as_txt(self):
        # Get items sorted in specified order:
        return '\n'.join(["%s: %s" % (item[0], item[1]) for item in self.attrs.iteritems()])

    def as_json(self):
        return self.attrs