import unittest
import json

from mock_service.shared import token_generator
from mock_service.shared import request_validator


class TestTokenGenerator(unittest.TestCase):

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


class TestRequestValidator(unittest.TestCase):

    def test_should_be_authorized_if_request_header_contains_authorization(self):
        authorized = request_validator.is_authorized({'authorization': 'Bearer this'})
        assert authorized

    def test_should_be_authorized_if_request_header_contains_authorization_with_bearer(self):
        authorized = request_validator.is_authorized({'authorization': 'Bearer this'})
        assert authorized

    def test_should_not_be_authorized_if_request_header_do_not_contain_authorization(self):
        authorized = request_validator.is_authorized({})
        assert not authorized

    def test_should_not_be_authorized_if_request_header_do_not_contain_bearer_in_authorization(self):
        authorized = request_validator.is_authorized({'authorization': 'this'})
        assert not authorized
