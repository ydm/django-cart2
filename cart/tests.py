# -*- coding: utf-8 -*-
# pylint: disable=W0212
# W0212: Access to a protected member

from __future__ import unicode_literals

from django.test import TestCase
from django.test import client

import cart
from cart import models


class CartTest(TestCase):

    def _cart(self):
        return cart.Cart(self._request().session)

    def _product(self, num):
        p = models.TestProduct(num=num)
        p.save()
        return p

    def _request(self):
        return client.Client()

    def setUp(self):
        pass

    def test_remove_different(self):
        c = self._cart()

        # Step 1: create some products in the db and add them in the
        # cart
        for i in range(10):
            c.add(self._product(i))
        
        # Step 2: take a part of the products we already have inside
        # the cart
        part = c._products(False)[5:]

        # Step 3: test if the products that are not members of `part`
        # are actually removed
        c.remove_different(part)
        self.assertEqual(part, c._products(False))
