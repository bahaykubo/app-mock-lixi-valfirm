import unittest

from validators.auth import authorized


class TestAuth(unittest.TestCase):

    def test_no_username_and_password_raises_value_error(self):
        try:
            result = authorized(None, None)
        except ValueError:
            assert True
        else:
            assert False

    def test_no_username_raises_value_error(self):
        try:
            result = authorized('username', None)
        except ValueError:
            assert True
        else:
            assert False

    def test_no_password_raises_value_error(self):
        try:
            result = authorized(None, 'password')
        except ValueError:
            assert True
        else:
            assert False

    def test_valid_username_password_returns_true(self):
        result = authorized('1platform', '1platform')
        assert result

    def test_incorrect_username_returns_false(self):
        result = authorized('incorrect', 'abvaluations')
        assert result is False

    def test_incorrect_password_returns_false(self):
        result = authorized('abvaluations', 'incorrect')
        assert result is False
