from django.test import TestCase
from django.contrib.auth.hashers import make_password
from web_app.models import User, Cart
from django.test import RequestFactory
from web_app.views import authentication


class AuthenticationTestCase(TestCase):
    def setUp(self):
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

        # Create admin user
        self.admin = User.objects.create(
            name="Test Admin",
            username="testadmin",
            password=make_password("testpassword"),
            account_type="A",
            avatar=None,
            share_wishlist=False
        )

    def test_sign_in_view(self):
        url = '/signin/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url, {'username': 'testuser', 'password': 'testpassword'})
        # Should be redirected to home page
        self.assertEqual(response.status_code, 302)

    def test_check_sign_in_view(self):
        url = '/check/signin/'
        response = self.client.post(
            url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'true')

    def test_sign_up_view(self):
        url = '/signup/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'name': 'New User',
            'username': 'newuser',
            'password': 'NewPassword123!',
            'accounttype': 'customer'
        })
        # Should be redirected to home page
        self.assertEqual(response.status_code, 302)

    def test_check_sign_up_view(self):
        url = '/check/signup/'
        response = self.client.post(url, {'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'true')

    def test_sign_out_view(self):
        url = '/signout/'
        response = self.client.get(url)
        # Should be redirected to home page
        self.assertEqual(response.status_code, 302)

    def test_view_accounts_view(self):
        # Create a request
        factory = RequestFactory()
        url = '/accounts/'
        request = factory.post(url)
        request.user = self.admin

        response = authentication.view_accounts(request)
        self.assertEqual(response.status_code, 200)

    def test_update_account_view(self):
        # Create a request
        factory = RequestFactory()
        url = '/account/update/' + str(self.user.id)
        request = factory.post(url, {'username-1': 'updateduser',
                               'password-1': 'UpdatedPassword123!', 'accounttype-1': 'customer'})
        request.user = self.admin

        response = authentication.update_account(request, str(self.user.id))
        # Should be redirected to accounts page
        self.assertEqual(response.status_code, 302)

    def test_delete_account_view(self):
        # Create a request
        factory = RequestFactory()
        url = '/account/delete/' + str(self.user.id)
        request = factory.post(url)
        request.user = self.admin

        response = authentication.delete_account(request, str(self.user.id))
        # Should be redirected to accounts page
        self.assertEqual(response.status_code, 302)
