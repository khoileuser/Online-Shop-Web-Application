from django.test import TestCase
from django.contrib.auth.hashers import make_password
from web_app.models import User, Cart, Product
from django.test import RequestFactory
from web_app.views import wishlist


class WishlistViewsTests(TestCase):
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
        self.cart = Cart.objects.create(owner=self.user)

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

    def test_view_wishlist_authenticated_user(self):
        url = '/wishlist/testuser'
        request = self.factory.get(url)
        request.user = self.user
        response = wishlist.view_wishlist(request, 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_view_wishlist_guest_user(self):
        url = '/wishlist/testuser'
        request = self.factory.get(url)
        request.user = 'guest'
        response = wishlist.view_wishlist(request, 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test User')

    def test_add_to_wishlist_authenticated_user(self):
        url = '/wishlist/add/' + str(self.product.id)
        request = self.factory.post(url, HTTP_REFERER='/wishlist/testuser')
        request.user = self.user
        response = wishlist.add_to_wishlist(request, self.product.id)
        # 302 is the status code for a successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.wishlist.filter(id=self.product.id).exists())

    def test_add_to_wishlist_guest_user(self):
        url = '/wishlist/add/' + str(self.product.id)
        request = self.factory.post(url, HTTP_REFERER='/wishlist/testuser')
        request.user = 'guest'
        response = wishlist.add_to_wishlist(request, self.product.id)
        # 302 is the status code for a successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin',
                             fetch_redirect_response=False)

    def test_remove_from_wishlist_authenticated_user(self):
        self.user.wishlist.add(self.product)
        url = '/wishlist/remove/' + str(self.product.id)
        request = self.factory.post(url, HTTP_REFERER='/wishlist/testuser')
        request.user = self.user
        response = wishlist.remove_from_wishlist(request, self.product.id)
        # 302 is the status code for a successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user.wishlist.filter(
            id=self.product.id).exists())

    def test_share_toggle_authenticated_user(self):
        url = '/wishlist/share/true'
        request = self.factory.post(url, HTTP_REFERER='/wishlist/testuser')
        request.user = self.user
        response = wishlist.share_toggle(request, 'true')
        # 302 is the status code for a successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(
            username='testuser').share_wishlist)
