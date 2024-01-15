from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from web_app.models import User, Cart
from django.test import RequestFactory
from web_app.views import me

import json


class MyAccountViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create(
            name="Test User",
            username="testuser",
            password=make_password("testpassword"),
            account_type="C",
            avatar=None,
            share_wishlist=False
        )
        self.cart = Cart.objects.create(owner=self.user)

    def test_my_account_view(self):
        url = '/me/'
        request = self.factory.get(url)
        request.user = self.user
        response = me.my_account(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_delete_account_view(self):
        url = '/me/delete/'
        request = self.factory.post(url)
        request.user = self.user
        response = None
        with self.assertRaises(AttributeError):
            response = me.delete_account(request)
            return
        if response:
            # Redirects after deleting account
            self.assertEqual(response.status_code, 302)
            self.assertFalse(User.objects.filter(
                username='testuser').exists())

    def test_update_account_name_view(self):
        url = '/me/update/name'
        request = self.factory.post(
            url, {'name': 'New Name'}, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.update_account(request, 'name')
        # Redirects after updating name
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(
            username='testuser').name, 'New Name')

    def test_update_account_password_view(self):
        url = '/me/update/password'
        request = self.factory.post(url, {
            'old-password': 'testpassword', 'new-password': 'newpassword'}, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.update_account(request, 'password')
        # Redirects after updating password
        self.assertEqual(response.status_code, 302)
        self.assertTrue(check_password(
            'newpassword', User.objects.get(username='testuser').password))

    # def test_update_account_avatar_view(self):
    #     # test update avatar, will add new file to static/images/avatar so uncomment if you want to test
    #     from os import getcwd
    #     with open(getcwd() + '/web_app/static/images/avatar/default.jpg', 'rb') as avatar_file:
    #         url = '/me/update/avatar'
    #         request = self.factory.post(
    #             url, {'avatar': avatar_file}, HTTP_REFERER='/me/')
    #         request.user = self.user
    #         response = me.update_account(request, 'avatar')
    #     # Redirects after updating avatar
    #     self.assertEqual(response.status_code, 302)
    #     user = User.objects.get(username='testuser')
    #     self.assertTrue(user.avatar)

    def test_get_states_view(self):
        url = '/states/get/US'
        request = self.factory.post(url)
        request.user = self.user
        response = me.get_states(request, 'US')
        self.assertEqual(response.status_code, 200)
        self.assertIn('California', json.loads(response.content))

    def test_address_add_view(self):
        url = '/me/address/add/'
        request = self.factory.post(url, {'phone_number_code': '+1', 'phone_number': '555-1234',
                                          'address': '123 Main St', 'city': 'City', 'state': 'CA', 'postal_code': '12345', 'country': 'USA'}, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.address_add(request)
        # Redirects after adding address
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(
            username='testuser').addresses.exists())

    def test_address_set_default_view(self):
        user = User.objects.get(username='testuser')
        address = user.addresses.create(phone_number_code='+1', phone_number='555-1234', address='123 Main St',
                                        city='City', state='CA', postal_code='12345', country='USA', is_default=False)

        url = '/me/address/set/default/' + str(address.id)
        request = self.factory.post(url, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.address_set_default(request, address.id)
        # Redirects after setting default address
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(
            username='testuser').addresses.get(id=address.id).is_default)

    def test_address_remove_view(self):
        user = User.objects.get(username='testuser')
        address = user.addresses.create(phone_number_code='+1', phone_number='555-1234', address='123 Main St',
                                        city='City', state='CA', postal_code='12345', country='USA', is_default=False)

        url = '/me/address/remove/' + str(address.id)
        request = self.factory.post(url, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.address_remove(request, address.id)
        # Redirects after removing address
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.get(
            username='testuser').addresses.filter(id=address.id).exists())

    def test_card_add_view(self):
        url = '/me/card/add/'
        request = self.factory.post(url, {'card_number': '4111111111111111', 'cardholder_name': 'Test User', 'expiration_date': '12/23',
                                          'card_type': 'Visa', 'cvc': '123'}, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.card_add(request)
        # Redirects after adding card
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(
            username='testuser').cards.exists())

    def test_card_set_default_view(self):
        user = User.objects.get(username='testuser')
        card = user.cards.create(card_number='4111111111111111', cardholder_name='Test User',
                                 expiration_date='12/23', card_type='Visa', cvc='123', is_default=False)

        url = '/me/card/set/default/' + str(card.id)
        request = self.factory.post(url, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.card_set_default(request, card.id)
        # Redirects after setting default card
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(
            username='testuser').cards.get(id=card.id).is_default)

    def test_card_remove_view(self):
        user = User.objects.get(username='testuser')
        card = user.cards.create(card_number='4111111111111111', cardholder_name='Test User',
                                 expiration_date='12/23', card_type='Visa', cvc='123', is_default=False)

        url = '/me/card/remove/' + str(card.id)
        request = self.factory.post(url, HTTP_REFERER='/me/')
        request.user = self.user
        response = me.card_remove(request, card.id)
        # Redirects after removing card
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.get(
            username='testuser').cards.filter(id=card.id).exists())
