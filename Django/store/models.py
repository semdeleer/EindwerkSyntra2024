"""
This module defines the Django models for an e-commerce application, including models for customers, products, orders, order items, and shipping addresses.

Classes:
    Customer: Represents a customer, with a one-to-one relationship to the Django User model.
    Product: Represents a product available for purchase.
    Order: Represents a customer's order, including its status and related properties.
    OrderItem: Represents an item within an order, linking a product to an order.
    ShippingAddress: Represents a shipping address associated with an order.

Each class includes appropriate fields and methods to manage and manipulate data within a Django application.

Classes:
    Customer:
        Fields:
            user (OneToOneField): A one-to-one relationship with the Django User model.
            name (CharField): The customer's name.
            email (CharField): The customer's email.
        
        Methods:
            __str__(): Returns the name of the customer.

    Product:
        Fields:
            name (CharField): The name of the product.
            price (FloatField): The price of the product.
            digital (BooleanField): Indicates if the product is digital.
            image (ImageField): The image of the product.
        
        Methods:
            __str__(): Returns the name of the product.
            imageURL (property): Returns the URL of the product's image if available.

    Order:
        Fields:
            customer (ForeignKey): A foreign key to the Customer model.
            date_ordered (DateTimeField): The date and time when the order was placed.
            complete (BooleanField): Indicates if the order is complete.
            transaction_id (CharField): The transaction ID for the order.
        
        Methods:
            __str__(): Returns the ID of the order.
            shipping (property): Returns True if any item in the order requires shipping.
            get_cart_total (property): Returns the total cost of all items in the cart.
            get_cart_items (property): Returns the total number of items in the cart.

    OrderItem:
        Fields:
            product (ForeignKey): A foreign key to the Product model.
            order (ForeignKey): A foreign key to the Order model.
            quantity (IntegerField): The quantity of the product in the order.
            date_added (DateTimeField): The date and time when the item was added to the order.
        
        Methods:
            get_total (property): Returns the total price for the quantity of the product.

    ShippingAddress:
        Fields:
            customer (ForeignKey): A foreign key to the Customer model.
            order (ForeignKey): A foreign key to the Order model.
            address (CharField): The shipping address.
            city (CharField): The city of the shipping address.
            state (CharField): The state of the shipping address.
            zipcode (CharField): The zip code of the shipping address.
            date_added (DateTimeField): The date and time when the address was added.
        
        Methods:
            __str__(): Returns the address.
"""

from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    """
    Represents a customer, with a one-to-one relationship to the Django User model.
    """
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents a product available for purchase.
    """
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        """
        Returns the URL of the product's image if available.
        """
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    """
    Represents a customer's order, including its status and related properties.
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        """
        Returns True if any item in the order requires shipping.
        """
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        """
        Returns the total cost of all items in the cart.
        """
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        """
        Returns the total number of items in the cart.
        """
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    """
    Represents an item within an order, linking a product to an order.
    """
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        """
        Returns the total price for the quantity of the product.
        """
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    """
    Represents a shipping address associated with an order.
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
