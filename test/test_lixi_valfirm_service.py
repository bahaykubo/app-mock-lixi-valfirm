import unittest
import requests


class TestLixiRequests(unittest.TestCase):

    def setUp(self):
        self.url = 'https://lixi-mock-valfirm-service.azurewebsites.net/mockvalfirm/'
        # self.url = 'http://localhost:8000/mockvalfirm/'
        self.headers = {'content-type': 'application/xml'}
        self.username = '1platform'
        self.password = '1platform'
        self.actions = ['Order', 'Update', 'Cancel', 'CancelAmend', 'AssignedValuer', 'Delay', 'FeeChange',
                        'NoteAdded', 'QuoteRequest', 'QuoteResponse', 'Error', 'Amendment', 'Escalate', 'Complete']
        self.packet = self._get_packet()

    def test_successful_soap_actions_message(self):
        for action in self.actions:
            payload = self._create_message(self.username, self.password, action, self.packet).encode('utf-8')
            response = requests.request('POST', self.url, data=payload, headers=self.headers)
            assert response.status_code == 200, f'Expecting 200 but got {response.status_code}'
            expected_response = '<tns:Result>0</tns:Result>'
            assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def test_only_put_method_allowed(self):
        methods = ['GET', 'PUT', 'DELETE']
        for method in methods:
            payload = self._create_message(self.username, self.password, 'Order', self.packet).encode('utf-8')
            response = requests.request(method, self.url, data=payload, headers=self.headers)
            assert response.status_code == 405, f'Expecting 405 but got {response.status_code}'

    def test_invalid_valuation_message(self):
        invalid_packet = '<xml>invalid</xml>'
        payload = self._create_message(self.username, self.password, 'Order', invalid_packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        assert response.status_code == 500, f'Expecting 500 but got {response.status_code}'
        expected_response = 'ValuationMessage is invalid'
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def test_invalid_soap_action_method(self):
        payload = self._create_message(self.username, self.password, 'Fail', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        assert response.status_code == 500, f'Expecting 500 but got {response.status_code}'
        expected_response = 'No matching global declaration available'
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def test_invalid_username(self):
        payload = self._create_message('invalid_username', self.password, 'Order', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        assert response.status_code == 500, f'Expecting 500 but got {response.status_code}'
        expected_response = 'Invalid authorisation'
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def test_invalid_password(self):
        payload = self._create_message(self.username, 'invalid_password', 'Order', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        assert response.status_code == 500, f'Expecting 500 but got {response.status_code}'
        expected_response = 'Invalid authorisation'
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def test_invalid_username_password(self):
        payload = self._create_message('invalid_username', 'invalid_password', 'Order', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        assert response.status_code == 500, f'Expecting 500 but got {response.status_code}'
        expected_response = 'Invalid authorisation'
        assert expected_response in response.text, f'Expecting "{expected_response}" but got "{response.text}"'

    def _create_message(self, username, password, action, packet):
        return f'''<?xml version="1.0" encoding="utf-8"?>
        <soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
            <soap-env:Header>
                <ns0:AuthHeader xmlns:ns0="lixi.mock.valfirm.service">
                    <ns0:UserName>{username}</ns0:UserName>
                    <ns0:Password>{password}</ns0:Password>
                </ns0:AuthHeader>
            </soap-env:Header>
            <soap-env:Body>
                <ns0:{action} xmlns:ns0="lixi.mock.valfirm.service">
                    <ns0:ValuationMessage><![CDATA[{packet}]]></ns0:ValuationMessage>
                </ns0:{action}>
            </soap-env:Body>
        </soap-env:Envelope>'''

    def _get_packet(self):
        with open('./test/files/lixi/valid_message.xml', 'r') as file:
            packet = file.read()
        return packet
