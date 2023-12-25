from django.db import models
from django.core.validators import MinLengthValidator


class Address(models.Model):
    phone_number_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)


class Cart(models.Model):
    CARD_TYPE_CHOICES = (
        ('VISA', 'Visa'),
        ('MC', 'Mastercard')
    )

    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiration_date = models.DateField()
    card_type = models.CharField(max_length=4, choices=CARD_TYPE_CHOICES)
    cvc = models.CharField(max_length=4)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.card_type} ending in {self.card_number[-4:]}"


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
    address = models.ManyToManyField(Address)
    card = models.ManyToManyField(Cart)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    images = models.JSONField(default=list, null=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, null=True)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct)


class Order(models.Model):
    ORDER_STATUSES = [
        ("A", "Active"),
        ("D", "Delivered"),
        ("C", "Canceled")
    ]
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(CartProduct)
    total_price = models.IntegerField()
    status = models.CharField(
        max_length=1, choices=ORDER_STATUSES, default="A")
