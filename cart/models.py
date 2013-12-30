# -*- coding: utf-8 -*-

# pylint: disable=W0232
# W0232: Class has no __init__ method

from __future__ import unicode_literals

import json
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property


@python_2_unicode_compatible
class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {}'.format(self.pk, self.created)


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


@python_2_unicode_compatible
class Item(models.Model):

    cart = models.ForeignKey(Cart)
    quantity = models.PositiveIntegerField()

    # Each item can store additional meta information.  For example if a
    # product has a variety of options (like the color of a t-shirt),
    # this is the place you need to store that when adding a new product
    # in the cart.  A simple API is built to work with that field and
    # you should never ever edit it manually.  For example if you want
    # to add a meta information to an existing item, use the following:
    #
    # item.meta['key'] = 'value'
    #
    # If you want to get that value later, use
    #
    # value = item.meta['key']
    metafld = models.TextField(default='{}', editable=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    product = generic.GenericForeignKey()

    class Meta:
        unique_together = ('cart', 'content_type', 'object_id')

    def __str__(self):
        return '{} x {}'.format(self.quantity, self.product)

    @cached_property
    def meta(self):
        return ItemMetaInformation(self, json.loads(self.metafld))


@python_2_unicode_compatible
class TestProduct(models.Model):
    num = models.IntegerField(unique=True)

    def __str__(self):
        return '{}'.format(self.num)
