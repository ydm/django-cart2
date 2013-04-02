# -*- coding: utf-8 -*-

# pylint: disable=W0141,W0142
# W0141: Used builtin function
# W0142: Used * or * magic*

# TODO: The Cart._products() method caches the results for better
# performance, but is not thread-safe.  1. Should it be?  2. If yes --
# make it.

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils import six

from cart import models


def cleanup(session):
    """Delete the cart that is currently stored in `session` and cleanup
    the database.

    """
    pk = session.pop('__cart__', None)
    if pk:
        try:
            cart = models.Cart.objects.get(pk=pk)
        except models.Cart.DoesNotExist:
            pass
        else:
            cart.delete()


class Cart(object):

    def __init__(self, session):
        self._cart = None

        self._cached_products = None
        self._modified = True

        cart = None
        pk = session.get('__cart__')
        if pk:
            try:
                cart = models.Cart.objects.get(pk=pk)
            except models.Cart.DoesNotExist:
                pass
        if not cart:
            cart = models.Cart()
            cart.save()
            session['__cart__'] = cart.pk
            if hasattr(session, 'modified'):
                session.modified = True
        self._cart = cart

    def __contains__(self, product):
        return product in self._products()

    def __iter__(self):
        return self._cart.item_set.iterator()

    def _item_for_product(self, product, qs=None):
        if qs is None:
            # Manager provides a proxy get() method
            qs = models.Item.objects 
        args = self._lookup_args(product)
        try:
            return qs.get(**args)
        except models.Item.DoesNotExist:
            return None

    def _items_for_products(self, products, qs=None):
        if qs is None:
            qs = models.Item.objects
        args = self._lookup_args(products[0])
        del args['object_id']
        args['object_id__in'] = [p.pk for p in products]
        return qs.filter(**args)

    def _lookup_args(self, product):
        return {
            'cart': self._cart,
            'content_type': ContentType.objects.get_for_model(type(product)),
            'object_id': product.pk
        }

    def _products(self, use_cache=True):
        if not use_cache or self._modified:
            self._cached_products = [item.product
                for item in self._cart.item_set.iterator()]
            self._modified = False
        return self._cached_products

    def add(self, product, quantity=1):
        args = self._lookup_args(product)
        args.update({'defaults': {'quantity': quantity}})
        item, created = models.Item.objects.get_or_create(**args)
        if not created and item.quantity != int(quantity):
            item.quantity = quantity
            item.save()
        self._modified = True

    @property
    def empty(self):
        """Return `True` if cart is empty."""
        return len(self._products()) == 0

    def incrby_quantity(self, product, value):
        """Add integer `value` to item.quantity atomically"""
        item = self._item_for_product(product,
                                      models.Item.objects.select_for_update())
        item.quantity += int(value)
        item.save()

    def quantity(self, product):
        item = self._item_for_product(product)
        return item.quantity if item else 0

    def remove(self, product):
        item = self._item_for_product(product)
        if item is not None:
            item.delete()
            self._modified = True

    def remove_all(self):
        self._cart.item_set.all().delete()
        self._modified = True

    def remove_different(self, products):
        """Remove all elements currently stored in this cart that are not part
        of the sequence `products`.

        """
        difference = filter(lambda p: p not in products, self._products())
        items = self._items_for_products(difference)
        items.delete()
        self._modified = True

    def set_products(self, products):
        """Update this cart using the data in `products`.  `products` should
        be a mapping in the following format:
        {product_object: quantity}.

        """
        # TODO: Can I actually optimize this routine?
        self.remove_all()
        for p, q in six.iteritems(products):
            self.add(p, q)

    @property
    def total(self):
        """Return the total number of products in this cart.  That is the sum
        of all the quantities.

        """
        return sum(item.quantity for item in
            self._cart.item_set.iterator())
