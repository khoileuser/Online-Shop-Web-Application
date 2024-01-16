from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.hashers import make_password

from web_app.models import User, Product, Review, Order
from web_app.views.product import *


class ProductTestCase(TestCase):
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

        self.vendor = User.objects.create(
            name="Test Vendor",
            username='testvendor',
            password=make_password("testpassword"),
            account_type='V',
            avatar=None,
            share_wishlist=False
        )

        # Create test products
        self.product1 = Product.objects.create(owner=self.vendor, name="Product 1", description="Description 1", price=50.00, stock=1, images=[
            "https://i.imgur.com/6VBx3io.png"], category="Luggage")
        self.product2 = Product.objects.create(
            owner=self.vendor, name="Product 2", description="Description 2", price=30.00, stock=1, category="Clothing")

        # Create test reviews
        self.review1 = Review.objects.create(
            author=self.user, product=self.product1, content='Great product!', rating=5)
        self.review2 = Review.objects.create(
            author=self.user, product=self.product2, content='Nice product', rating=4)

        # Create test orders
        self.address = self.user.addresses.create(phone_number_code='+1', phone_number='555-1234', address='123 Main St',
                                                  city='City', state='CA', postal_code='12345', country='USA', is_default=False)
        self.card = self.user.cards.create(card_number='4111111111111111', cardholder_name='Test User',
                                           expiration_date='12/23', card_type='Visa', cvc='123', is_default=False)

        self.order = Order.objects.create(
            owner=self.user, status='D', address=self.address, card=self.card, total_price=2.0)
        self.order.products.create(product=self.product1, quantity=1)
        self.order.products.create(product=self.product2, quantity=1)

    def test_listing_view(self):
        url = '/products/'
        request = self.factory.get(url)
        request.user = self.user
        response = listing(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

    def test_view_product(self):
        url = '/products/' + str(self.product1.id) + '/'
        request = self.factory.get(url)
        request.user = self.user
        response = view_product(request, self.product1.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Great product!')

    def test_add_review_view(self):
        url = '/products/review/' + str(self.product1.id) + '/'
        request = self.factory.post(url, {'content': 'Excellent!', 'stars': 5})
        request.user = self.user
        response = add_review(request, self.product1.id)
        # Expecting a redirect after adding a review
        self.assertEqual(response.status_code, 302)

    def test_listing_vendor_view(self):
        url = '/products/vendor/' + self.vendor.username + '/'
        request = self.factory.get(url)
        request.user = self.vendor
        response = listing_vendor(request, self.vendor.username)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

    def test_add_product_view(self):
        url = '/products/add/'
        request = self.factory.post(url, {'pd-name': 'New Product', 'pd-price': 40.0, 'img-range': 0,
                                    'pd-category': 'Books', 'pd-description': 'New Description', 'pd-stock': 20})
        request.user = self.vendor
        response = add_product(request)
        # Expecting a redirect after adding a product
        self.assertEqual(response.status_code, 302)

    # def test_update_product_view(self):
    #     # delete actual images on local storage, backup product 2 images before running this test
    #     url = '/products/update/' + str(self.product2.id) + '/'
    #     request = self.factory.post(url, {'pd-name': 'Updated Product', 'pd-price': 60.0, 'img-range': 0, 'pd-category': 'other',
    #                                 'pd-new-category': 'Electronics', 'pd-description': 'Updated Description', 'pd-stock': 15})
    #     request.user = self.vendor
    #     response = update_product(request, self.product2.id)
    #     # Expecting a redirect after updating a product
    #     self.assertEqual(response.status_code, 302)

    # def test_delete_product_view(self):
    #     # delete actual images on local storage, backup product 2 images before running this test
    #     url = '/products/delete/' + str(self.product2.id) + '/'
    #     request = self.factory.post(url)
    #     request.user = self.vendor
    #     response = delete_product(request, self.product2.id)
    #     # Expecting a redirect after deleting a product
    #     self.assertEqual(response.status_code, 302)
