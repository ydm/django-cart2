# -*- coding: utf-8 -*-

# pylint: disable=W0232
# W0232: Class has no __init__ method

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    checked_out = models.BooleanField(default=False)

    @python_2_unicode_compatible
    def __str__(self):
        return '{}, {}'.format(self.pk, self.created)


class Item(models.Model):

    cart = models.ForeignKey(Cart)
    quantity = models.PositiveIntegerField()

    product_type = models.ForeignKey(ContentType)
    product_id = models.PositiveIntegerField()
    _product = generic.GenericForeignKey('product_type', 'product_id')

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ('cart',)
        unique_together = ('cart', 'product_type', 'product_id')

    @python_2_unicode_compatible
    def __str__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self.product_type = ContentType.objects.get_for_model(value)
        self.product_id = value.pk
