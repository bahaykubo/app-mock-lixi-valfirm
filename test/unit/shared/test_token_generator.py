from django.test import TestCase
import json

from mock_service.shared import token_generator


class TestTokenGenerator(TestCase):

    def test_should_contain_an_access_token(self):
        token = json.loads(token_generator.generate_token_dictionary())
        assert token['access_token']

    def test_should_contain_a_token_type(self):
        token = json.loads(token_generator.generate_token_dictionary())
        assert token['token_type']

    def test_should_contain_a_bearer_token_type(self):
        token = json.loads(token_generator.generate_token_dictionary())
        assert token['token_type'] == 'Bearer'

    def test_should_contain_an_expiry_time(self):
        token = json.loads(token_generator.generate_token_dictionary())
        assert token['expires_in']
