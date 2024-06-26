"""
This module contains utility functions for handling shopping cart operations in our Django e-commerce application.

Functions:
    cookieCart(request):
        Creates a cart for non-logged-in users using cookies. 
        Returns the cart items, order summary, and shipping information.

    cartData(request):
        Retrieves cart data for authenticated users from the database and for non-authenticated users from cookies.
        Returns the cart items, order summary, and shipping information.

    guestOrder(request, data):
        Handles order creation for guest users. 
        Creates a customer and order based on the information provided in the form data.
        Returns the customer and order objects.
"""

import json
from .models import *

def cookieCart(request):
    """
    Create an empty cart for non-logged-in users using cookies.

    Args:
        request (HttpRequest): The request object containing the cookies.

    Returns:
        dict: A dictionary containing the cart items, order summary, and shipping information.
    """
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            if cart[i]['quantity'] > 0:  # items with negative quantity = lot of freebies
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = product.price * cart[i]['quantity']

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price, 'imageURL': product.imageURL}, 
                    'quantity': cart[i]['quantity'],
                    'digital': product.digital, 
                    'get_total': total,
                }
                items.append(item)

                if not product.digital:
                    order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    """
    Retrieve cart data for authenticated users from the database and for non-authenticated users from cookies.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict: A dictionary containing the cart items, order summary, and shipping information.
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    """
    Handle order creation for guest users. Create a customer and order based on the information provided in the form data.

    Args:
        request (HttpRequest): The request object.
        data (dict): The form data containing customer information.

    Returns:
        tuple: A tuple containing the customer and order objects.
    """
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'] if item['quantity'] > 0 else -1 * item['quantity'],  # negative quantity = freebies
        )
    return customer, order
