import unittest
from lxml import etree
from io import StringIO

from lixi_mock_valfirm_service.service.validators.valuation_message import authorized, valid_message


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


class TesXMLMessage(unittest.TestCase):

    def setUp(self):
        self.schema = './lixi_mock_valfirm_service/service/files/ValuationTransaction_1_6.xsd'

    def test_message_returns_true(self):
        with open('./lixi_mock_valfirm_service/service/files/valid_message.xml', 'r') as file:
            xml_string = file.read()
        xml = etree.fromstring(xml_string)
        result = valid_message(xml, self.schema)
        assert result is True

    def test_invalid_valuation_message_returns_false(self):
        invalid_xml = etree.fromstring('<xml>invalid</xml>')
        result = valid_message(invalid_xml, self.schema)
        assert result is False

    def test_empty_valuation_message_raises_value_error(self):
        try:
            result = valid_message(None, self.schema)
        except ValueError:
            assert True
        else:
            assert False

    def test_incorrect_type_message_returns_false(self):
        try:
            xml_doc = etree.parse('./lixi_mock_valfirm_service/service/files/valid_message.xml')
            result = valid_message(xml_doc, self.schema)
        except TypeError:
            assert True
        else:
            assert False

    def test_no_schema_raises_type_error(self):
        try:
            with open('./lixi_mock_valfirm_service/service/files/valid_message.xml', 'r') as file:
                xml_string = file.read()
            xml = etree.fromstring(xml_string)
            result = valid_message(xml, None)
        except TypeError:
            assert True
        else:
            assert False
