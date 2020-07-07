import unittest
from lxml import etree

import config
from mock_service.lixi_valfirm.validators.valuation_message import authorized, valid_message


class TestAuthorisation(unittest.TestCase):

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

    def test_incorrect_username_password_returns_false(self):
        result = authorized('incorrect', 'incorrect')
        assert result is False


class TesXMLMessage(unittest.TestCase):

    def setUp(self):
        self.schema = config.SCHEMA_FILE

    def test_message_returns_true(self):
        with open('./files/valid_message.xml', 'r') as file:
            xml_string = file.read()
        result = valid_message(xml_string, self.schema)

    def test_invalid_valuation_message_returns_false(self):
        result = valid_message('<xml>invalid</xml>', self.schema)
        assert result is False

    def test_empty_valuation_message_raises_value_error(self):
        try:
            result = valid_message(None, self.schema)
        except ValueError:
            assert True
        else:
            assert False

    def test_invalid_message_returns_false(self):
        with open('./files/invalid_message.xml', 'r') as file:
            xml_string = file.read()
        result = valid_message(xml_string, self.schema)
        assert result is False

    def test_incorrect_type_message_raises_value_error(self):
        try:
            with open('./files/valid_message.xml', 'r') as file:
                xml_string = file.read()
            xml = etree.XML(xml_string)
            result = valid_message(xml, self.schema)
        except ValueError:
            assert True
        else:
            assert False

    def test_no_schema_raises_type_error(self):
        try:
            with open('./files/valid_message.xml', 'r') as file:
                xml_string = file.read()
            result = valid_message(xml_string, None)
        except TypeError:
            assert True
        else:
            assert False
