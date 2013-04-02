# -*- coding: utf-8 -*-

# pylint: disable=W0232
# W0232: Class has no __init__ method

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {}'.format(self.pk, self.created)


@python_2_unicode_compatible
class Item(models.Model):

    cart = models.ForeignKey(Cart)
    quantity = models.PositiveIntegerField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    product = generic.GenericForeignKey()

    class Meta:
        unique_together = ('cart', 'content_type', 'object_id')

    def __str__(self):
        return '{} x {}'.format(self.quantity, self.product)


@python_2_unicode_compatible
class TestProduct(models.Model):
    num = models.IntegerField(unique=True)

    def __str__(self):
        return '{}'.format(self.num)
