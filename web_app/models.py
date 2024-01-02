from django.db import models
from django.core.validators import MinLengthValidator


# The Address class represents a model with fields for phone number code, phone number, address, city,
# state, postal code, country, and a boolean field for default address.
class Address(models.Model):
    phone_number_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=12)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)


# The Card class represents a credit card with attributes such as card number, cardholder name,
# expiration date, card type, cvc, and a flag indicating if it is the default card.
class Card(models.Model):
    CARD_TYPE_CHOICES = (
        ('VISA', 'Visa'),
        ('MC', 'Mastercard')
    )

    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiration_date = models.CharField(max_length=5)
    card_type = models.CharField(max_length=4, choices=CARD_TYPE_CHOICES)
    cvc = models.CharField(max_length=4)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.card_type} ending in {self.card_number[-4:]}"


# The User class represents a user in a system with attributes such as tokens, username, password,
# name, avatar, account type, cart quantity, addresses, and cards.
class User(models.Model):
    ACCOUNT_TYPES = [
        ("V", "Vendor"),
        ("C", "Customer"),
        ("S", "Shipper")
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
    addresses = models.ManyToManyField(Address)
    cards = models.ManyToManyField(Card)
    wishlist = models.ManyToManyField("Product")


# The above class represents a Product model with fields for owner, name, price, images, description,
# and category.
class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    images = models.JSONField(default=list, null=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, null=True)


# The CartProduct class represents a product in a shopping cart with a reference to the product and
# the quantity of that product.
class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


# The Cart class represents a shopping cart owned by a user and contains a collection of CartProduct
# objects.
class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct)


# The Order class represents an order made by a user, containing information such as the owner,
# products, address, card, total price, and status.
class Order(models.Model):
    ORDER_STATUSES = [
        ("A", "Active"),
        ("G", "Delivering"),
        ("D", "Delivered"),
        ("C", "Canceled")
    ]
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(CartProduct)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField()
    status = models.CharField(
        max_length=1, choices=ORDER_STATUSES, default="A")
