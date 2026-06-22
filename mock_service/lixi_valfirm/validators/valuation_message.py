from lxml import etree


def valid_message(xml_string, schema):
    schema_doc = etree.parse(schema)
    schema = etree.XMLSchema(schema_doc)
    try:
        xml = etree.XML(xml_string)
    except TypeError as e:
        raise ValueError(str(e)) from e
    result = schema.validate(xml)
    return result


def authorized(username, password):
    if all(input is None for input in [username, password]):
        raise ValueError('no username and password provided')
    elif any(input is None for input in [username, password]):
        raise ValueError('no username or password provided')
    elif username == '1platform' and password == '1platform':
        result = True
    else:
        result = False
    return result
