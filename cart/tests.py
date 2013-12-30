# -*- coding: utf-8 -*-
# pylint: disable=W0212
# W0212: Access to a protected member

from __future__ import unicode_literals

from django.test import TestCase
from django.test import client

import cart
from cart import models
from cart.meta import serialize


class CartTest(TestCase):

    def _cart(self):
        """Return always a fresh cart"""
        cart.cleanup(self._request().session)
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

    def test_add_meta(self):
        c = self._cart()

        # Add some products with meta information attached to them
        for i in range(10):
            c.add(self._product(i), meta={'i': i})

        # Check if they're all stored correctly
        for i, item in enumerate(c):
            self.assertEqual(i, item.meta['i'])

        # Change all product metas and assert with a separate query that
        # it's correctly stored into the databse
        for i, item in enumerate(c):
            item.meta['i'] = i * 2

        # Check if everything's correct
        for i, item in enumerate(c):
            self.assertEqual(i * 2, item.meta['i'])

    def test_meta_db(self):
        c = self._cart()
        for i in range(10):
            p = self._product(i)
            c.add(p, meta={'i': i})

            # Run a manual query to assert everything in the database is
            # correctly stored
            sql = 'SELECT * FROM cart_item WHERE id={}'.format(p.pk)

            rawitem = models.TestProduct.objects.raw(sql)[0]
            expected = serialize({'i': i})
            actual = rawitem.metafld
            self.assertEqual(expected, actual)

            # Now change the meta value and rerun the same query
            c.set_meta(p, 'i', i*2)

            rawitem2 = models.TestProduct.objects.raw(sql)[0]
            expected2 = serialize({'i': i*2})
            actual2 = rawitem2.metafld
            self.assertEqual(expected2, actual2)
