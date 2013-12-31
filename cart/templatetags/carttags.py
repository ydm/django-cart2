# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from json import dumps
from django import template


register = template.Library()

@register.simple_tag
def cart_quantity(cart, product):
    return cart.quantity(product)


@register.simple_tag
def cart_meta_as_json(cart, product):
    meta = cart.meta_for_product(product)
    if meta is not None:
        return dumps(meta.as_dict())
    return '{}'
