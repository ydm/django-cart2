Cart2
-----

Simple cart package for Django.

It was sequentially maintained by:
* Eric Woudenberg
* Marc Garcia
* Bruno Carvalho

I made a fork and enriched it by adding features.  All the code is
rewritten with Python 3 compliance in mind.  Python2 is supported
using the django.utils.six package which is part of Django as of
version 1.5.

The cart is successfully used in a real-world shop without any problems so far.

##Prerequisites
* Django 1.5
* Django Content Types app
* Django Session app

##Installation
1. Add `'cart'` to `INSTALLED_APPS`
2. Run `./manage.py syncdb`

##Guide

####Create a cart for current session
```python
import cart

session = request.session or {}
c = cart.Cart(session)```

####Add/Remove products from cart
```python
# Add a product
product = myapp.models.Product.objects.get(pk=product_pk)
quantity = 10
c.add(product, quantity)

# Remove a product
product = myapp.models.Product.objects.get(pk=product_pk)
c.remove(product)```

####Quantity methods
```python
# Check quantity of product
quantity_of_product = c.quantity(product)

# Increase quantity by one
# Please note that incrby_quantity doesn't check the quantity value
new_quantity = c.incrby_quantity(product, 1)

# Decrease quantity by 2
new_quantity = c.incrby_quantity(product, 2)```

####Batch operations
```python
product_pks = [1, 2, 3, 4, 5]
product_qts = [6, 7, 8, 9, 10]
products = {
    myapp.models.Product.objects.get(pk=pk) : qt
    for pk, qt in zip(product_pks, product_qts)
}

# Add products at once
c.add_products(products)

# Leave just these products in cart and remove all other
products = myapp.models.Product.objects.filter(pk__in=[1,2,3])
c.remove_different(products)

# Update the cart (by removing all existing products and adding just the new ones)
c.set_products(products)

# Remove all products
c.remove_all()```

####State
```python
# Check if the cart is empty
if c.empty:
    # empty
else:
    # not empty

# Get the total number of products inside the cart
total_numbers_in_cart = c.total```

####Use in templates
First you have to add the `'cart.context_processors.add_cart'` to your
`TEMPLATE_CONTEXT_PROCESSORS` list.

```html
{% if cart.empty %}
    <h1>Your cart is empty</h1>
{% else %}
    <h1>You have {{ cart.total }} products in your cart</h1>
    <ul>
        {% for item in cart %}
            <li>{{ item.quantity }} x {{ item.product }}</li>
        {% endfor %}
    </ul>
{% endif %}```

####Template tags
There is a simple template-tag you can use to check the quantity of a
product (given you have just the product object at hand).
```html
{% load carttags %}
<h1>{{ product }}</h1>
{% if product in cart %}
    <p>You have {% cart_quantity cart product %} products of this
       type inside your cart.</p>
{% else %}
    <p>This product is not in your cart</p>
{% endif %}```

###Why it's not on PyPi
Actually the original cart is right there under the name
`django-cart`.

The interface 

Anyway, I don't think that's a serious enough project to take up space
there for a cloning with just minor updates as this one.  The license
is LGPL and you're fully free to fork/copy the code and create a
package on your own, if you need such a thing.  Suit yourself.

I plan to maintain this cart right here as long as I need it in my
work.

###Known problems
A lot.  It uses the db a lot and makes unnecessary queries.
