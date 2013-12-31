# -*- coding: utf-8 -*-

# pylint: disable=W0141,W0142
# W0141: Used builtin function
# W0142: Used * or * magic*

# TODO: The Cart._products() method caches the results for better
# performance, but is not thread-safe.  1. Should it be?  2. If yes --
# make it.

from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType
from django.utils import six

from cart import models
from cart.meta import serialize


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


@python_2_unicode_compatible
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

    def __str__(self):
        return '\n'.join(
            '{} x {}'.format(item.quantity, item.product) for item in self
        )

    def meta_for_product(self, product):
        """Return a dictionary or None."""
        item = self._item_for_product(product)
        return item.meta if item else None

    def set_meta(self, product, key, value):
        """Return True on success, False otherwise."""
        meta = self.meta_for_product(product)
        if meta:
            meta[key] = value
            return True
        return False

    def get_meta(self, product, key):
        """Return the keyed meta value for this product or None."""
        meta = self.meta_for_product(product)
        return meta[key] if meta else None

    def add(self, product, quantity=1, meta=None):
        """Add or update a product.  If `meta` is None, existing meta
        information aren't changed at all.  If you want to delete
        current meta using this method, pass '{}' as `meta` value.

        """
        serialized = serialize(meta)
        args = self._lookup_args(product)
        args.update({'defaults': {'quantity': quantity, 
                                  'metafld': serialized}})
        item, created = models.Item.objects.get_or_create(**args)
        if not created:
            item.quantity = quantity
            if meta is not None:
                item.metafld = serialized
            item.save()
        self._modified = True

    def add_products(self, products):
        """Add given products to cart.

        Arguments:
        - `products`: a dictionary of product objects mapped to
          quantities.  For example:
          { <Product: A product>       : 1,
            <Product: Another product> : 2 }

        """
        # TODO: Can I actually optimize this and insert them all at
        # once?
        return [self.add(p, q) for p, q in products.items()]

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
        return item.quantity

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
        diff = list(filter(lambda p: p not in products, self._products()))
        if diff:
            items = self._items_for_products(diff)
            items.delete()
            self._modified = True

    def set_products(self, products):
        """Update this cart using the data in `products`.  `products` should
        be a mapping in the following format:
        {product_object: quantity}.

        TODO y: Let's support meta information with this method.

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
