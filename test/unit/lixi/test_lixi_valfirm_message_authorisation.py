from django.test import TestCase

from mock_service.lixi_valfirm.validators.valuation_message import authorized


class TestAuthorisation(TestCase):

    def setUp(self):
        self.authorized = authorized

    def test_no_username_and_password_raises_value_error(self):
        try:
            self.authorized(None, None)
        except ValueError:
            assert True
        else:
            assert False

    def test_no_username_raises_value_error(self):
        try:
            self.authorized('username', None)
        except ValueError:
            assert True
        else:
            assert False

    def test_no_password_raises_value_error(self):
        try:
            self.authorized(None, 'password')
        except ValueError:
            assert True
        else:
            assert False

    def test_valid_username_password_returns_true(self):
        result = self.authorized('1platform', '1platform')
        assert result

    def test_incorrect_username_returns_false(self):
        result = self.authorized('incorrect', 'abvaluations')
        assert result is False

    def test_incorrect_password_returns_false(self):
        result = self.authorized('abvaluations', 'incorrect')
        assert result is False

    def test_incorrect_username_password_returns_false(self):
        result = self.authorized('incorrect', 'incorrect')
        assert result is False
