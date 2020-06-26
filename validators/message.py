from lxml import etree


def validate(xml_string, schema):
    schema_doc = etree.parse(schema)
    schema = etree.XMLSchema(schema_doc)
    xml = etree.ElementTree(xml_string)
    result = schema.validate(xml)
    return result
