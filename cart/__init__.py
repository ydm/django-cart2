# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cart import models


class Cart:

    def __init__(self, request):
        cart = None
        pk = request.session.get('__cart__')
        if pk:
            try:
                cart = models.Cart.objects.get(pk=pk)
            except models.Cart.DoesNotExist:
                pass
        if not cart:
            cart = models.Cart()
            cart.save()
            request.session['__cart__'] = cart.pk
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all().iterator():
            yield item

    def add(self, product, quantity=1):
        defaults = {'quantity': quantity}
        item, created = models.Item.objects.get_or_created(
            cart=self.cart, product=product, defaults=defaults)
        if not created:
            item.quantity = quantity
            item.save()

    def incrby_quantity(self, product, value):
        """Add integer `value` to item.quantity atomically"""
        item = models.Item.objects.select_for_update().get(
            cart=self.cart, product=product)
        item.quantity += int(value)
        item.save()

    def remove(self, product):
        item = models.Item.objects.get(cart=self.cart, product=product)
        item.delete()

    def count(self):
        return sum(item.quantity for item in self.cart.item_set.all())
        
    def remove_all(self):
        for item in self.cart.item_set.all():
            item.delete()
