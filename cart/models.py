# -*- coding: utf-8 -*-

# pylint: disable=W0232
# W0232: Class has no __init__ method

from __future__ import unicode_literals

import json
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from cart.meta import ItemMetaInformation


@python_2_unicode_compatible
class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {}'.format(self.pk, self.created)


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

    def get_product_price(self):
        if not hasattr(settings, 'CART_GET_PRODUCT_PRICE'):
            from django.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(
                'You need to set `CART_GET_PRODUCT_PRICE` in your settings'
                'before you can use the Item.get_product_price() method.'
            )
        fqname = settings.CART_GET_PRODUCT_PRICE
        from django.utils import importlib
        index = fqname.rindex('.')
        modulename = fqname[:index]
        funcname = fqname[index+1:]
        module = importlib.import_module(modulename)
        func = getattr(module, funcname)
        return func(self)

    @cached_property
    def meta(self):
        return ItemMetaInformation(self, json.loads(self.metafld))


@python_2_unicode_compatible
class TestProduct(models.Model):
    num = models.IntegerField(unique=True)

    def __str__(self):
        return '{}'.format(self.num)
