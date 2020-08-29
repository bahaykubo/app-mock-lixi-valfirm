import unittest
import os
import copy
from django.http import QueryDict
import requests

from mock_service.mocktrack import views


class TestMocktrackRequests(unittest.TestCase):

    def setUp(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mock_service.settings')

        self.xml = f'''<?xml version="1.0" encoding="utf-8"?>
            <hometrack>
                <realtime accountid="123456">
                    <valuationrequest>
                        <property reference="CTT-EA49-CRF" propertytype="3" streetnum="86" street="oriel"
                            streettype="road" suburb="ivanhoe" postcode="4242" state="nsw"
                            estimatedvalue="485000"/>
                    </valuationrequest>
                </realtime>
            </hometrack>'''

        self.xml_address_only = f'''<?xml version="1.0" encoding="utf-8"?>
            <hometrack>
                <realtime accountid="123456">
                    <valuationrequest>
                        <property reference="CTT-EA49-CRF" propertytype="4" postcode="5120"
                            address="7 FOREST COURT, VIRGINIA, SA 5120" />
                    </valuationrequest>
                </realtime>
            </hometrack>'''

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
            }}

        self.request_parameters = {
            'fuseaction': 'api.interface',
            'accountid': '13265',
            'password': 'AbCdEfG1234',
            'autologin': 'ThisIsMyLOGIN',
            'autopassword': 'th1sIsMyPWord',
            'realtimevalauth': 'abc'
        }

        self.action = {
            'account_id': '13265'
        }

    def set_url(self, action, env=None):
        return f'https://{"localhost:8000" if env == "local" else "lixi-mock-valfirm-service.azurewebsites.net"}/mocktrack/index.cfm?fuseaction={"api.interface" if action == "api" else "api.retrievevaluationpdf"}&accountid=13265&password=AbCdEfG1234&autologin=ThisIsMyLOGIN&autopassword=th1sIsMyPWord&realtimevalauth=abc'

    def test_get_is_allowed_request_method(self):
        assert views.allowed_request_method('get')

    def test_post_is_allowed_request_method(self):
        assert views.allowed_request_method('post')

    def test_not_allowed_request_method(self):
        assert not views.allowed_request_method('put'), 'put should not be an allowed request method'
        assert not views.allowed_request_method('delete'), 'delete should not be an allowed request method'

    def test_valid_xml_to_dictionary(self):
        dictionary = views.convert_xml_request_to_dictionary(self.xml)
        assert type(dictionary) is dict, f'expecting a dictionary if xml is valid but got {type(dictionary)}'

    def test_invalid_xml_to_dictionary_raises_syntax_error(self):
        try:
            dictionary = views.convert_xml_request_to_dictionary('<bing></bong>')
        except SyntaxError:
            assert True, 'syntax error should be raised with an invalid xml'

    def test_complete_address(self):
        assert views.address_complete(self.property_request)

    def test_incomplete_address_no_property(self):
        property = copy.deepcopy(self.property_request)
        del property['property']
        assert not views.address_complete(property)

    def test_incomplete_address_no_streetnum(self):
        property = copy.deepcopy(self.property_request)
        del property['property']['streetnum']
        assert not views.address_complete(property)

    def test_incomplete_address_no_street(self):
        property = copy.deepcopy(self.property_request)
        del property['property']['street']
        assert not views.address_complete(property)

    def test_incomplete_address_no_streettype(self):
        property = copy.deepcopy(self.property_request)
        del property['property']['streettype']
        assert not views.address_complete(property)

    def test_incomplete_address_no_suburb(self):
        property = copy.deepcopy(self.property_request)
        del property['property']['suburb']
        assert not views.address_complete(property)

    def test_incomplete_address_no_postcode(self):
        property = copy.deepcopy(self.property_request)
        del property['property']['postcode']
        assert not views.address_complete(property)

    def test_incomplete_address_no_state(self):
        property = copy.deepcopy(self.property_request)
        del property['property']['state']
        assert not views.address_complete(property)

    def test_valid_request_parameters(self):
        get = QueryDict(mutable=True)
        get.update(self.request_parameters)
        action = views.validate_request_and_get_action(get)
        assert action['account_id'] == self.request_parameters['accountid']

    def test_valid_api_request_parameters(self):
        get = QueryDict(mutable=True)
        get.update(self.request_parameters)
        action = views.validate_request_and_get_action(get)
        assert action['fuseaction'] == 'api'

    def test_valid_pdf_request_parameters(self):
        pdf_request_parameter = copy.deepcopy(self.request_parameters)
        pdf_request_parameter['fuseaction'] = 'api.retrievevaluationpdf'

        get = QueryDict(mutable=True)
        get.update(pdf_request_parameter)
        action = views.validate_request_and_get_action(get)
        assert action['fuseaction'] == 'pdf'

    def test_invalid_request_parameters_raises_permission_error(self):
        pdf_request_parameter = copy.deepcopy(self.request_parameters)
        del pdf_request_parameter['accountid']

        get = QueryDict(mutable=True)
        get.update(pdf_request_parameter)
        try:
            action = views.validate_request_and_get_action(get)
        except PermissionError:
            assert True

    def test_api_request_action_returns_xml_response(self):
        xml = views.api_response(self.property_request, self.action)
        assert f'realtimevaluation="{self.property_request["property"]["estimatedvalue"]}"' in xml

    def test_api_request_action_2m_autoupgrade_returns_xml_response(self):
        property_request = copy.deepcopy(self.property_request)
        property_request['property']['estimatedvalue'] = '489042'

        xml = views.api_response(property_request, self.action)
        assert f'realtimevaluation="2500042"' in xml

    def test_error_response(self):
        xml = views.error_response('1', 'expect this error message')
        assert f'errorid="1" errormessage="expect this error message"' in xml

    def test_mocktrack_api_request_response(self):
        response = requests.post(self.set_url('api'), data=self.xml)
        assert response.status_code == 200, f'Expecting 200 but got {response.status_code}'
        assert '/xml' in response.headers['Content-Type'], f'Expecting xml content but got {response.headers}'

    def test_mocktrack_pdf_request_response(self):
        response = requests.post(self.set_url('pdf'), data=self.xml)
        assert response.status_code == 200, f'Expecting 200 but got {response.status_code}'
        assert '/pdf' in response.headers['Content-Type'], f'Expecting pdf content but got {response.headers}'
