import json
from django.test import TestCase

from mock_service.shared import token_generator


class TestTokenGenerator(TestCase):

    def setUp(self):
        self.token = json.loads(token_generator.generate_token_dictionary())

    def test_should_contain_an_access_token(self):
        self.assertIn('access_token', self.token)

    def test_should_contain_a_token_type(self):
        self.assertIn('token_type', self.token)

    def test_should_contain_a_bearer_token_type(self):
        self.assertEqual(self.token['token_type'], 'Bearer')

    def test_should_contain_an_expiry_time(self):
        self.assertIn('expires_in', self.token)
