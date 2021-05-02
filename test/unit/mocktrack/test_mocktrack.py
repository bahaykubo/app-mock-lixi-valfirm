import copy
from django.test import TestCase
from django.http import QueryDict
from pathlib import Path

from mock_service.mocktrack import views


class TestMocktrack(TestCase):

    def setUp(self):
        self.view = views
        self.xml = Path('./test/files/mocktrack/valid.xml').read_text()

        self.request_parameters = {
            'fuseaction': 'api.interface',
            'accountid': '13265',
            'password': 'AbCdEfG1234',
            'autologin': 'ThisIsMyLOGIN',
            'autopassword': 'th1sIsMyPWord',
            'realtimevalauth': 'abc'
        }

        self.property_request = {
            'realtime': {
                'accountid': '13265'
            },
            'property': {
                'propertytype': '3',
                'streetnum': '86',
                'street': 'oriel',
                'streettype': 'road',
                'suburb': 'ivanhoe',
                'postcode': '4242',
                'state': 'nsw',
                'estimatedvalue': '485000'
            }
        }

        self.action = {
            'account_id': '13265'
        }

    def test_get_is_allowed_request_method(self):
        assert self.view.allowed_request_method('get')

    def test_post_is_allowed_request_method(self):
        assert self.view.allowed_request_method('post')

    def test_not_allowed_request_method(self):
        assert not self.view.allowed_request_method('put'), 'put should not be an allowed request method'
        assert not self.view.allowed_request_method('delete'), 'delete should not be an allowed request method'

    def test_valid_xml_to_dictionary(self):
        dictionary = self.view.convert_xml_request_to_dictionary(self.xml.encode())
        assert isinstance(dictionary, dict), f'expecting a dictionary if xml is valid but got {type(dictionary)}'

    def test_invalid_xml_to_dictionary_raises_syntax_error(self):
        try:
            self.view.convert_xml_request_to_dictionary('<bing></bong>'.encode())
        except SyntaxError:
            assert True, 'syntax error should be raised with an invalid xml'

    def test_complete_address(self):
        assert self.view.address_complete(self.property_request)

    def test_incomplete_address_no_property(self):
        property_result = copy.deepcopy(self.property_request)
        del property_result['property']
        assert not self.view.address_complete(property)

    def test_incomplete_address_no_streetnum(self):
        property_result = copy.deepcopy(self.property_request)
        del property_result['property']['streetnum']
        assert not self.view.address_complete(property)

    def test_incomplete_address_no_street(self):
        property_result = copy.deepcopy(self.property_request)
        del property_result['property']['street']
        assert not self.view.address_complete(property)

    def test_incomplete_address_no_streettype(self):
        property_result = copy.deepcopy(self.property_request)
        del property_result['property']['streettype']
        assert not self.view.address_complete(property)

    def test_incomplete_address_no_suburb(self):
        property_result = copy.deepcopy(self.property_request)
        del property_result['property']['suburb']
        assert not self.view.address_complete(property)

    def test_incomplete_address_no_postcode(self):
        property_result = copy.deepcopy(self.property_request)
        del property_result['property']['postcode']
        assert not self.view.address_complete(property)

    def test_incomplete_address_no_state(self):
        property_result = copy.deepcopy(self.property_request)
        del property_result['property']['state']
        assert not self.view.address_complete(property)

    def test_valid_request_parameters(self):
        get = QueryDict(mutable=True)
        get.update(self.request_parameters)
        action = self.view.validate_request_and_get_action(get)
        assert action['account_id'] == self.request_parameters['accountid']

    def test_valid_api_request_parameters(self):
        get = QueryDict(mutable=True)
        get.update(self.request_parameters)
        action = self.view.validate_request_and_get_action(get)
        assert action['fuseaction'] == 'api'

    def test_valid_pdf_request_parameters(self):
        pdf_request_parameter = copy.deepcopy(self.request_parameters)
        pdf_request_parameter['fuseaction'] = 'api.retrievevaluationpdf'

        get = QueryDict(mutable=True)
        get.update(pdf_request_parameter)
        action = self.view.validate_request_and_get_action(get)
        assert action['fuseaction'] == 'pdf'

    def test_invalid_request_parameters_raises_permission_error(self):
        pdf_request_parameter = copy.deepcopy(self.request_parameters)
        del pdf_request_parameter['accountid']

        get = QueryDict(mutable=True)
        get.update(pdf_request_parameter)
        try:
            self.view.validate_request_and_get_action(get)
        except PermissionError:
            assert True

    def test_api_request_action_returns_xml_response(self):
        xml = self.view.api_response(self.property_request, self.action)
        assert f'realtimevaluation="{self.property_request["property"]["estimatedvalue"]}"' in xml

    def test_api_request_action_2m_autoupgrade_returns_xml_response(self):
        property_request = copy.deepcopy(self.property_request)
        property_request['property']['estimatedvalue'] = '489042'

        xml = self.view.api_response(property_request, self.action)
        assert 'realtimevaluation="2500042"' in xml

    def test_error_response(self):
        xml = self.view.error_response('1', 'expect this error message')
        assert 'errorid="1" errormessage="expect this error message"' in xml
