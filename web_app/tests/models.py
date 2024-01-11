from django.test import TestCase
from web_app.models import *


class AddressTestCase(TestCase):
    def setUp(self):
        Address.objects.create(phone_number_code="1", phone_number="1234567890", address="123 Main St",
                               city="New York", state="NY", postal_code="12345", country="USA", is_default=True)

    def test_address(self):
        address = Address.objects.get(phone_number_code="1")
        self.assertEqual(address.phone_number_code, "1")
        self.assertEqual(address.phone_number, "1234567890")
        self.assertEqual(address.address, "123 Main St")
        self.assertEqual(address.city, "New York")
        self.assertEqual(address.state, "NY")
        self.assertEqual(address.postal_code, "12345")
        self.assertEqual(address.country, "USA")
        self.assertEqual(address.is_default, True)


class CardTestCase(TestCase):
    def setUp(self):
        Card.objects.create(card_number="1234567890123456", cardholder_name="John Doe", expiration_date="12/25",
                            card_type="VISA", cvc="123", is_default=True)

    def test_card(self):
        card = Card.objects.get(card_number="1234567890123456")
        self.assertEqual(card.card_number, "1234567890123456")
        self.assertEqual(card.cardholder_name, "John Doe")
        self.assertEqual(card.expiration_date, "12/25")
        self.assertEqual(card.card_type, "VISA")
        self.assertEqual(card.cvc, "123")
        self.assertEqual(card.is_default, True)


class UserTestCase(TestCase):
    def setUp(self):
        address = Address.objects.create(phone_number_code="1", phone_number="1234567890", address="123 Main St",
                                         city="New York", state="NY", postal_code="12345", country="USA", is_default=True)
        card = Card.objects.create(card_number="1234567890123456", cardholder_name="John Doe", expiration_date="12/25",
                                   card_type="VISA", cvc="123", is_default=True)

        user = User.objects.create(username="johndoecustomer", password="password", name="John Doe Customer", avatar="https://i.imgur.com/6VBx3io.png",
                                   account_type="C", cart_quantity=0, share_wishlist=False)
        user.addresses.add(address)
        user.cards.add(card)

    def test_user(self):
        user = User.objects.get(username="johndoecustomer")
        self.assertEqual(user.username, "johndoecustomer")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.name, "John Doe Customer")
        self.assertEqual(user.avatar, "https://i.imgur.com/6VBx3io.png")
        self.assertEqual(user.account_type, "C")
        self.assertEqual(user.cart_quantity, 0)
        self.assertEqual(user.share_wishlist, False)
        self.assertEqual(user.addresses.all()[0].phone_number_code, "1")
        self.assertEqual(user.cards.all()[0].card_number, "1234567890123456")


class ProductTestCase(TestCase):
    def setUp(self):
        owner = User.objects.create(username="johndoevendor", password="password",
                                    name="John Doe Vendor", avatar="https://i.imgur.com/6VBx3io.png", account_type="V", cart_quantity=0, share_wishlist=False)
        Product.objects.create(owner=owner, name="Product", description="Description", price=1.00, stock=1, images=[
                               "https://i.imgur.com/6VBx3io.png"], category="Category")

    def test_product(self):
        product = Product.objects.get(name="Product")
        self.assertEqual(product.owner.username, "johndoevendor")
        self.assertEqual(product.name, "Product")
        self.assertEqual(product.description, "Description")
        self.assertEqual(product.price, 1.00)
        self.assertEqual(product.stock, 1)
        self.assertEqual(product.images, ["https://i.imgur.com/6VBx3io.png"])
        self.assertEqual(product.category, "Category")


class ReviewTestCase(TestCase):
    def setUp(self):
        vendor = User.objects.create(username="johndoevendor", password="password", name="John Doe Vendor",
                                     avatar="https://i.imgur.com/6VBx3io.png", account_type="V", cart_quantity=0, share_wishlist=False)
        product = Product.objects.create(owner=vendor, name="Product", description="Description", price=1.00, stock=1, images=[
                                         "https://i.imgur.com/6VBx3io.png"], category="Category")
        author = User.objects.create(username="johndoecustomer", password="password", name="John Doe Customer", avatar="https://i.imgur.com/6VBx3io.png",
                                     account_type="C", cart_quantity=0, share_wishlist=False)
        Review.objects.create(author=author, rating=0.0,
                              content="Content", product=product)

    def test_review(self):
        product = Product.objects.get(name="Product")
        review = Review.objects.get(product=product)
        self.assertEqual(review.author.username, "johndoecustomer")
        self.assertEqual(review.rating, 0.0)
        self.assertEqual(review.content, "Content")
        self.assertEqual(review.product.name, "Product")


class CartProductTestCase(TestCase):
    def setUp(self):
        vendor = User.objects.create(username="johndoevendor", password="password", name="John Doe Vendor",
                                     avatar="https://i.imgur.com/6VBx3io.png", account_type="V", cart_quantity=0, share_wishlist=False)
        product = Product.objects.create(owner=vendor, name="Product", description="Description", price=1.00, stock=1, images=[
                                         "https://i.imgur.com/6VBx3io.png"], category="Category")
        CartProduct.objects.create(product=product, quantity=1)

    def test_cart_product(self):
        cart_product = CartProduct.objects.get(quantity=1)
        self.assertEqual(cart_product.product.name, "Product")
        self.assertEqual(cart_product.quantity, 1)


class CartTestCase(TestCase):
    def setUp(self):
        vendor = User.objects.create(username="johndoevendor", password="password", name="John Doe Vendor",
                                     avatar="https://i.imgur.com/6VBx3io.png", account_type="V", cart_quantity=0, share_wishlist=False)
        product = Product.objects.create(owner=vendor, name="Product", description="Description", price=1.00, stock=1, images=[
            "https://i.imgur.com/6VBx3io.png"], category="Category")
        cart_product = CartProduct.objects.create(product=product, quantity=1)

        owner = User.objects.create(username="johndoecustomer", password="password",
                                    name="John Doe Customer", avatar="https://i.imgur.com/6VBx3io.png", account_type="C", cart_quantity=0, share_wishlist=False)
        cart = Cart.objects.create(owner=owner)
        cart.products.add(cart_product)

    def test_cart(self):
        owner = User.objects.get(username="johndoecustomer")
        cart = Cart.objects.get(owner=owner)
        self.assertEqual(cart.owner.username, "johndoecustomer")
        self.assertEqual(cart.products.all()[0].product.name, "Product")


class OrderTestCase(TestCase):
    def setUp(self):
        vendor = User.objects.create(username="johndoevendor", password="password", name="John Doe Vendor",
                                     avatar="https://i.imgur.com/6VBx3io.png", account_type="V", cart_quantity=0, share_wishlist=False)
        product = Product.objects.create(owner=vendor, name="Product", description="Description", price=1.00, stock=1, images=[
            "https://i.imgur.com/6VBx3io.png"], category="Category")
        cart_product = CartProduct.objects.create(product=product, quantity=1)

        owner = User.objects.create(username="johndoecustomer", password="password",
                                    name="John Doe Customer", avatar="https://i.imgur.com/6VBx3io.png", account_type="C", cart_quantity=0, share_wishlist=False)
        address = Address.objects.create(phone_number_code="1", phone_number="1234567890", address="123 Main St",
                                         city="New York", state="NY", postal_code="12345", country="USA", is_default=True)
        card = Card.objects.create(card_number="1234567890123456", cardholder_name="John Doe", expiration_date="12/25",
                                   card_type="VISA", cvc="123", is_default=True)

        order = Order.objects.create(
            owner=owner, address=address, card=card, total_price=0)
        order.products.add(cart_product)
        total_price = 0
        for cart_product in order.products.all():
            total_price += cart_product.product.price
        order.total_price = total_price
        order.save()

    def test_order(self):
        owner = User.objects.get(username="johndoecustomer")
        order = Order.objects.get(owner=owner)
        self.assertEqual(order.owner.username, "johndoecustomer")
        self.assertEqual(order.address.phone_number_code, "1")
        self.assertEqual(order.card.card_number, "1234567890123456")
        self.assertEqual(order.products.all()[0].product.name, "Product")
        self.assertEqual(order.total_price, 1.00)
