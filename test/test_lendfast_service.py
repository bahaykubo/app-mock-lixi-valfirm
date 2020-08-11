import unittest
import requests
import json


class TestLendfastRequests(unittest.TestCase):

    def setUp(self):
        self.url = 'https://lixi-mock-valfirm-service.azurewebsites.net/mocklender/'
        # self.url = 'http://localhost:8000/mocklender/'
        self.headers = {'content-type': 'application/xml'}
        self.token_url = 'https://lixi-mock-valfirm-service.azurewebsites.net/as/token.oauth2'
        # self.token_url = 'http://localhost:8000/as/token.oauth2'
        self.token_headers = {'content-type': 'application/x-www-form-urlencoded'}

        self.packet = '<q1:notificationList xmlns:q1="http://www.sandstone-vms.com.au/schema/vms/1.0"><q1:notification type="StatusChange" timestamp="2020-05-29T12:57:27.2581866"><Identifier UniqueID="cf456220-cc3a-4dfd-8ddd-7714dfec69f1" Description="Notification ID" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction" /><Identifier UniqueID="LCA-ET4R-RET" Description="Valuation ID" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction" /><Status Name="Accepted" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction"><Date>2020-05-29</Date><Time>12:57:00.0000000+10:00</Time></Status></q1:notification></q1:notificationList>'

        self.invalid_packet = '<q1:XnotificationList xmlns:q1="http://www.sandstone-vms.com.au/schema/vms/1.0"><q1:notification type="StatusChange" timestamp="2020-05-29T12:57:27.2581866"><Identifier UniqueID="cf456220-cc3a-4dfd-8ddd-7714dfec69f1" Description="Notification ID" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction" /><Status Name="Accepted" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction"></Status></q1:notification></q1:XnotificationList>'

    def test_oath2_returns_dummy_token(self):
        response = requests.post(self.token_url, headers=self.token_headers)
        assert response.status_code == 200, f'Expecting 200 but got {response.status_code}'
        token = json.loads(response.text)
        assert token['access_token'], f'No access token on response "{token}"'

    def test_oath2_only_put_method_allowed(self):
        response = requests.get(self.token_url, headers=self.token_headers)
        assert response.status_code == 405, f'Expecting 405 but got {response.status_code} for get method'

        response = requests.put(self.token_url, headers=self.token_headers)
        assert response.status_code == 405, f'Expecting 405 but got {response.status_code} for put method'

        response = requests.delete(self.token_url, headers=self.token_headers)
        assert response.status_code == 405, f'Expecting 405 but got {response.status_code} for delete method'

    def test_lender_successful_soap_message(self):
        response = requests.request('POST', self.url, data=self.packet, headers=self.headers)
        assert response.status_code == 200, f'Expecting 200 but got {response.status_code}'
        expected_response = 'acknowledge'
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def test_only_put_method_allowed(self):
        methods = ['GET', 'PUT', 'DELETE']
        for method in methods:
            response = requests.request(method, self.url, data=self.packet, headers=self.headers)
            assert response.status_code == 400, f'Expecting 400 but got {response.status_code}'

    def test_invalid_message(self):
        invalid_packet = '<xml>invalid</xml>'
        response = requests.request('POST', self.url, data=invalid_packet, headers=self.headers)
        assert response.status_code == 404, f'Expecting 404 but got {response.status_code}'
        expected_response = "Requested resource 'xml' not found"
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def test_invalid_soap_action_method(self):
        response = requests.request('POST', self.url, data=self.invalid_packet, headers=self.headers)
        assert response.status_code == 404, f'Expecting 404 but got {response.status_code}'
        expected_response = 'not found'
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'
