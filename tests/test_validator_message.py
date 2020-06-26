import unittest
from lxml import etree
from io import StringIO

from validators.valuation_message import valid_message


class TesMessage(unittest.TestCase):

    def setUp(self):
        self.schema = './files/ValuationTransaction_1_6.xsd'

    def test_message_returns_true(self):
        with open('./files/valid_message.xml', 'r') as file:
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
            xml_doc = etree.parse('./files/valid_message.xml')
            result = valid_message(xml_doc, self.schema)
        except TypeError:
            assert True
        else:
            assert False

    def test_no_schema_raises_type_error(self):
        try:
            with open('./files/valid_message.xml', 'r') as file:
                xml_string = file.read()
            xml = etree.fromstring(xml_string)
            result = valid_message(xml, None)
        except TypeError:
            assert True
        else:
            assert False
