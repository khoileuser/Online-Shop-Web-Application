from django.db import models


class User(models.Model):
    ACCOUNT_TYPES = [
        ("V", "Vendor"),
        ("C", "Customer")
    ]
    tokens = models.JSONField(default=list, null=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255, null=True)
    account_type = models.CharField(
        max_length=1, choices=ACCOUNT_TYPES)
    cart_quantity = models.IntegerField(default=0)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    images = models.JSONField(default=list, null=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, null=True)


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = [{
        'product': models.ManyToManyField(Product),
        'quantity': models.IntegerField()
    }]
    total_price = models.IntegerField()


class Order(models.Model):
    ORDER_STATUSES = [
        ("A", "Active"),
        ("D", "Delivered"),
        ("C", "Canceled")
    ]
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    products = [{
        'product': models.ManyToManyField(Product),
        'quantity': models.IntegerField()
    }]
    total_price = models.IntegerField()
    status = []
