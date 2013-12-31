# -*- coding: utf-8 -*-

import json


class ItemMetaInformation(object):
    def __init__(self, instance, d):
        self.instance = instance
        self.d = d

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value
        self.instance.metafld = json.dumps(self.d)
        # TODO y: I should check when Django commits changes to the
        # database and fix this if it causes the ORM to issue a database
        # query every time a property is set
        self.instance.save()

    def __delitem__(self, key):
        raise NotImplementedError

    def as_dict(self):
        return self.d.copy()


def serialize(obj):
    obj = obj or {}
    # TODO y: Check if object is dictionary
    return json.dumps(obj)


def deserialize(s):
    s = s or '{}'
    # TODO y: Check if object is string and raise a TypeError if not
    return json.loads(s)
