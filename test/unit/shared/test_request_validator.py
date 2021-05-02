from django.test import TestCase

from mock_service.shared import request_validator


class TestRequestValidator(TestCase):

    def setUp(self):
        self.validator = request_validator

    def test_should_be_authorized_if_request_header_contains_authorization(self):
        authorized = self.validator.is_authorized({'authorization': 'Bearer this'})
        self.assertTrue(authorized)

    def test_should_be_authorized_if_request_header_contains_authorization_with_bearer(self):
        authorized = self.validator.is_authorized({'authorization': 'Bearer this'})
        self.assertTrue(authorized)

    def test_should_not_be_authorized_if_request_header_do_not_contain_authorization(self):
        authorized = self.validator.is_authorized({})
        self.assertFalse(authorized)

    def test_should_not_be_authorized_if_request_header_do_not_contain_bearer_in_authorization(self):
        authorized = self.validator.is_authorized({'authorization': 'this'})
        self.assertFalse(authorized)
