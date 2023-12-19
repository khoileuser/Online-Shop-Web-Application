from django.db import models
from django.core.validators import MinLengthValidator


class User(models.Model):
    ACCOUNT_TYPES = [
        ("V", "Vendor"),
        ("C", "Customer")
    ]
    tokens = models.JSONField(default=list, null=True)
    username = models.CharField(max_length=25, unique=True, validators=[
                                MinLengthValidator(4, "Usernames must be between 4 and 25 characters.")])
    password = models.TextField()
    name = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255, null=True)
    account_type = models.CharField(
        max_length=1, choices=ACCOUNT_TYPES)
    cart_quantity = models.IntegerField(default=0)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    images = models.JSONField(default=list, null=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, null=True)


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = [{
        'product': models.ManyToManyField(Product),
        'quantity': models.IntegerField()
    }]
    total_price = models.FloatField()


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
    status = models.CharField(
        max_length=1, choices=ORDER_STATUSES, default="A")
