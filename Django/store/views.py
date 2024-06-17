"""
This module contains views for handling e-commerce operations in our Django application, including 
rendering pages, updating the shopping cart, and processing orders.

Functions:
    index(request):
        Renders the homepage of the store.

    login(request):
        Renders the login page.

    store(request):
        Renders the store page with product listings and cart information.

    cart(request):
        Renders the cart page with current cart items and order summary.

    checkout(request):
        Renders the checkout page with current cart items and order summary.

    updateItem(request):
        Handles adding and removing items from the cart. Updates the cart quantities and returns a JSON response.

    processOrder(request):
        Processes the order by creating or updating customer and order details. Handles both authenticated and guest users.
"""

from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder


def index(request):
    """
    Renders the homepage of the store.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered homepage.
    """
    return render(request, 'store/index.html')

def login(request):
    """
    Renders the login page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered login page.
    """
    return render(request, 'store/login.html')

def store(request):
    """
    Renders the store page with product listings and cart information.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered store page with product listings and cart information.
    """
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    """
    Renders the cart page with current cart items and order summary.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered cart page with current cart items and order summary.
    """
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    """
    Renders the checkout page with current cart items and order summary.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered checkout page with current cart items and order summary.
    """
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    """
    Handles adding and removing items from the cart. Updates the cart quantities and returns a JSON response.

    Args:
        request (HttpRequest): The request object containing the product ID and action.

    Returns:
        JsonResponse: A response indicating that the item was added or removed.
    """
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    """
    Processes the order by creating or updating customer and order details. Handles both authenticated and guest users.

    Args:
        request (HttpRequest): The request object containing order and shipping details.

    Returns:
        JsonResponse: A response indicating that the payment was submitted.
    """
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
