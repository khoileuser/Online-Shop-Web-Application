from django.test import TestCase


class CommonViewsTests(TestCase):
    def setUp(self):
        pass

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_terms_view(self):
        response = self.client.get('/terms/')
        self.assertEqual(response.status_code, 200)

    def test_privacy_view(self):
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)

    def test_execute_view(self):
        response = self.client.get('/execute/')
        self.assertEqual(response.status_code, 200)
