# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json


def serialize(obj):
    obj = obj or {}
    # TODO y: Check if object is dictionary
    return json.dumps(obj)


def deserialize(s):
    s = s or '{}'
    # TODO y: Check if object is string and raise a TypeError if not
    return json.loads(s)
