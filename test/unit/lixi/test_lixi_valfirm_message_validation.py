from django.test import TestCase
from lxml import etree

from mock_service.lixi_valfirm import config
from mock_service.lixi_valfirm.validators.valuation_message import valid_message


class TestXMLMessage(TestCase):

    def setUp(self):
        self.schema = config.SCHEMA_FILE
        self.valid_message = valid_message

    def test_message_returns_true(self):
        with open('./test/files/lixi/valid_message.xml', 'r') as file:
            xml_string = file.read()
        self.valid_message(xml_string, self.schema)

    def test_invalid_valuation_message_returns_false(self):
        result = self.valid_message('<xml>invalid</xml>', self.schema)
        assert result is False

    def test_empty_valuation_message_raises_value_error(self):
        try:
            self.valid_message(None, self.schema)
        except ValueError:
            assert True
        else:
            assert False

    def test_invalid_message_returns_false(self):
        with open('./test/files/lixi/invalid_message.xml', 'r') as file:
            xml_string = file.read()
        result = self.valid_message(xml_string, self.schema)
        assert result is False

    def test_incorrect_type_message_raises_value_error(self):
        try:
            with open('./test/files/lixi/valid_message.xml', 'r') as file:
                xml_string = file.read()
            xml = etree.XML(xml_string)
            self.valid_message(xml, self.schema)
        except ValueError:
            assert True
        else:
            assert False

    def test_no_schema_raises_type_error(self):
        try:
            with open('./test/files/lixi/valid_message.xml', 'r') as file:
                xml_string = file.read()
            self.valid_message(xml_string, None)
        except TypeError:
            assert True
        else:
            assert False
