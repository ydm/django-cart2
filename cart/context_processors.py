# -*- coding: utf-8 -*-
# Thanks to https://github.com/thedod/django-cart/blob/master/cart
# /context_processors.py for the idea

from __future__ import unicode_literals

from django.conf import settings

from cart import Cart


def add_cart(request):
    """Include cart in context data"""
    return {'cart': Cart(request)}
