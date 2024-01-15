from django.test import TestCase
from web_app.models import User, Cart, Product
from django.test import RequestFactory
from web_app.views import cart


class CartViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create(
            name="Test User",
            username='testuser',
            password='testpassword',
            account_type='C',
            avatar=None,
            share_wishlist=False
        )
        self.cart = Cart.objects.create(owner=self.user)

        self.vendor = User.objects.create(
            name="Test Vendor",
            username='testvendor',
            password='testpassword',
            account_type='V',
            avatar=None,
            share_wishlist=False
        )
        self.product = Product.objects.create(owner=self.vendor, name="Product", description="Description", price=1.00, stock=1, images=[
            "https://i.imgur.com/6VBx3io.png"], category="Category")

    def test_view_cart_authenticated_customer(self):
        url = '/cart/'
        request = self.factory.get(url)
        request.user = self.user
        response = cart.view_cart(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cart')

    def test_view_cart_unauthenticated_user(self):
        url = '/cart/'
        request = self.factory.get(url)
        request.user = 'guest'
        response = cart.view_cart(request)
        self.assertRedirects(response, '/signin',
                             fetch_redirect_response=False)

    def test_add_to_cart_authenticated_customer(self):
        url = '/cart/add/' + str(self.product.id) + '/quantity/1'
        request = self.factory.post(url)
        request.user = self.user
        response = cart.add_to_cart(request, self.product.id, 1)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'cart_plus': True})
        self.assertEqual(self.user.cart_quantity, 1)

    def test_add_to_cart_unauthenticated_user(self):
        url = '/cart/add/' + str(self.product.id) + '/quantity/1'
        request = self.factory.post(url)
        request.user = 'guest'
        response = cart.add_to_cart(request, self.product.id, 1)
        self.assertJSONEqual(response.content, {'signin': True})

    def test_remove_from_cart_authenticated_customer(self):
        self.cart.products.create(product=self.product, quantity=2)
        self.user.cart_quantity = 1
        url = '/cart/remove/' + str(self.product.id) + '/quantity/1'
        request = self.factory.post(url)
        request.user = self.user
        response = cart.remove_from_cart(request, self.product.id, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.products.all()[0].quantity, 1)
        self.assertEqual(self.user.cart_quantity, 1)

    def test_remove_all_from_cart_authenticated_customer(self):
        self.cart.products.create(product=self.product, quantity=2)
        self.user.cart_quantity = 1
        url = '/cart/remove/' + str(self.product.id) + '/quantity/2'
        request = self.factory.post(url)
        request.user = self.user
        response = cart.remove_from_cart(request, self.product.id, 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.products.count(), 0)
        self.assertEqual(self.user.cart_quantity, 0)

    def test_remove_from_cart_unauthenticated_user(self):
        url = '/cart/remove/' + str(self.product.id) + '/quantity/1'
        request = self.factory.post(url)
        request.user = 'guest'
        response = cart.remove_from_cart(request, self.product.id, 1)
        self.assertRedirects(response, '/signin',
                             fetch_redirect_response=False)
