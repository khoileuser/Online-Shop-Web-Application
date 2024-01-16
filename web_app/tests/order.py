from django.test import TestCase
from django.contrib.auth.hashers import make_password
from web_app.models import User, Cart, Product, Order, Address, Card
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from web_app.views.order import *


class CheckoutTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create a user for testing
        self.user = User.objects.create(
            name="Test User",
            username="testuser",
            password=make_password("testpassword"),
            account_type="C",
            avatar=None,
            share_wishlist=False
        )

        # Create some sample data for testing
        self.vendor = User.objects.create(
            name="Test Vendor",
            username='testvendor',
            password=make_password("testpassword"),
            account_type='V',
            avatar=None,
            share_wishlist=False
        )
        self.product = Product.objects.create(owner=self.vendor, name="Product", description="Description", price=1.00, stock=1, images=[
            "https://i.imgur.com/6VBx3io.png"], category="Category")

        self.cart = Cart.objects.create(owner=self.user)
        self.cart_product = self.cart.products.create(
            product=self.product, quantity=2)
        self.address = self.user.addresses.create(phone_number_code='+1', phone_number='555-1234', address='123 Main St',
                                                  city='City', state='CA', postal_code='12345', country='USA', is_default=False)
        self.card = self.user.cards.create(card_number='4111111111111111', cardholder_name='Test User',
                                           expiration_date='12/23', card_type='Visa', cvc='123', is_default=False)

    def test_get_vendors(self):
        # Test get_vendors function
        vendors = get_vendors([self.cart_product])
        self.assertEqual(len(vendors), 1)
        self.assertEqual(vendors[0], self.vendor)

    def test_get_products_by_vendor(self):
        # Test get_products_by_vendor function
        products_by_vendor = get_products_by_vendor(
            [self.vendor], [self.cart_product])
        self.assertEqual(len(products_by_vendor), 1)
        self.assertEqual(products_by_vendor[0]['vendor']['id'], self.vendor.id)
        self.assertEqual(
            products_by_vendor[0]['cart_products'][0]['product']['id'], self.product.id)

    def test_calc_total_price(self):
        # Test calc_total_price function
        total_price = calc_total_price([self.cart_product])
        self.assertEqual(total_price, 2.0)

    def test_parse_checkout_context_all(self):
        # Test parse_checkout_context function with mode='all'
        url = '/checkout/'
        request = self.factory.post(url, {'mode': 'all'})
        request.user = self.user
        context = parse_checkout_context(request, 'all')
        self.assertEqual(context['mode'], 'all')
        self.assertEqual(context['total_price'], 2.0)

    def test_checkout_view(self):
        # Test checkout view
        url = '/checkout/'
        request = self.factory.get(url, {'mode': 'all'})
        request.user = self.user

        # Add session to the request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        response = checkout(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Checkout', response.content.decode())
