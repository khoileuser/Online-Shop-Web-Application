from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.middleware import SessionMiddleware

from web_app.models import User, Cart, Product
from web_app.views.order import *

from re import search
from json import loads


class CheckoutTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create users for testing
        self.user = User.objects.create(
            name="Test User",
            username="testuser",
            password=make_password("testpassword"),
            account_type="C",
            avatar=None,
            share_wishlist=False
        )

        self.vendor = User.objects.create(
            name="Test Vendor",
            username='testvendor',
            password=make_password("testpassword"),
            account_type='V',
            avatar=None,
            share_wishlist=False
        )

        self.shipper = User.objects.create(
            name="Test Shipper",
            username='testshipper',
            password=make_password("testpassword"),
            account_type='S',
            avatar=None,
            share_wishlist=False
        )

        # Create some sample data for testing
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

    def test_checkout_get_view(self):
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

    def test_place_order_all(self):
        request = self.factory.post('/place_order/', {'mode': 'all'})
        request.user = self.user

        # Add session to the request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        # Add context to the session
        request.session['context'] = {
            'address': {'id': self.address.id},
            'card': {'id': self.card.id},
            'mode': 'all'
        }

        response = place_order(request)
        self.assertEqual(response.status_code, 200)

        # Decode the bytes to a string and parse it as JSON
        data = loads(response.content.decode())

        # Check if the redirected URL matches the expected pattern
        match = search(r'^/order/\d+/?$', data['redirectUrl'])
        self.assertIsNotNone(
            match, "Redirected URL does not match expected pattern")

    def test_order_view(self):
        order = Order.objects.create(owner=self.user, status='A', address=self.address,
                                     card=self.card, total_price=2.0)
        order.products.set(self.cart.products.all())
        url = '/order/' + str(order.id) + '/'
        request = self.factory.get(url)
        request.user = self.user
        response = view_order(request, order.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Active')

    def test_orders_view(self):
        order = Order.objects.create(owner=self.user, status='A', address=self.address,
                                     card=self.card, total_price=2.0)
        order.products.set(self.cart.products.all())
        url = '/orders/'
        request = self.factory.get(url)
        request.user = self.user
        response = view_orders(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Orders')

    def test_orders_shipper_view(self):
        order = Order.objects.create(owner=self.user, status='A', address=self.address,
                                     card=self.card, total_price=2.0)
        order.products.set(self.cart.products.all())
        url = '/orders/'
        request = self.factory.get(url)
        request.user = self.shipper
        response = view_orders(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Set status')
