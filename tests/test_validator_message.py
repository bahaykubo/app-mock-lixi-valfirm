import unittest
from lxml import etree
from io import StringIO
from validators.message import validate


class TesMessage(unittest.TestCase):

    def setUp(self):
        self.schema = './files/ValuationTransaction_1_6.xsd'

    def test_message_returns_true(self):
        xml_doc = etree.parse('./files/valid_message.xml')
        xml = etree.XMLParser(xml_doc)
        result = validate(xml, self.schema)
        assert result is True

    def test_invalid_valuation_message_returns_false(self):
        invalid_xml = '<xml>invalid</xml>'
        result = validate(invalid_xml, self.schema)
        assert result is False

    def test_empty_valuation_message_raises_value_error(self):
        try:
            result = validate(None, self.schema)
        except ValueError:
            assert True
        else:
            assert False

    def test_non_string_type_message_returns_false(self):
        try:
            xml_doc = etree.parse('./files/valid_message.xml')
            result = validate(xml_doc, self.schema)
        except ValueError:
            assert True
        else:
            assert False

    def test_no_schema_raises_type_error(self):
        try:
            # xml_doc = etree.parse('./files/valid_message.xml')
            xml = etree.tostring(StringIO('./files/valid_message.xml'))
            result = validate(xml, None)
        except TypeError:
            assert True
        else:
            assert False
