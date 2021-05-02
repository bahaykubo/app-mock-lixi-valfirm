from unittest import TestCase
import requests

from test import config


class TestLixi(TestCase):

    def setUp(self):
        self.url = f'{config.hostname()}/mockvalfirm/'
        self.headers = {'content-type': 'application/xml'}
        self.username = '1platform'
        self.password = '1platform'
        self.actions = ['Order', 'Update', 'Cancel', 'CancelAmend', 'AssignedValuer', 'Delay', 'FeeChange',
                        'NoteAdded', 'QuoteRequest', 'QuoteResponse', 'Error', 'Amendment', 'Escalate', 'Complete']
        self.packet = self._get_packet()

    def test_successful_soap_actions_message(self):
        for action in self.actions:
            payload = self._create_message(self.username, self.password, action, self.packet).encode('utf-8')
            response = requests.post(self.url, data=payload, headers=self.headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<tns:Result>0</tns:Result>', response.text)

    def test_only_put_method_allowed(self):
        methods = ['GET', 'PUT', 'DELETE']
        for method in methods:
            payload = self._create_message(self.username, self.password, 'Order', self.packet).encode('utf-8')
            response = requests.request(method, self.url, data=payload, headers=self.headers)
            self.assertEqual(response.status_code, 405)

    def test_invalid_valuation_message(self):
        invalid_packet = '<xml>invalid</xml>'
        payload = self._create_message(self.username, self.password, 'Order', invalid_packet).encode('utf-8')
        response = requests.post(self.url, data=payload, headers=self.headers)
        self.assertEqual(response.status_code, 500)
        self.assertIn('ValuationMessage is invalid', response.text)

    def test_invalid_soap_action_method(self):
        payload = self._create_message(self.username, self.password, 'Fail', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        self.assertEqual(response.status_code, 500)
        self.assertIn('No matching global declaration available', response.text)

    def test_invalid_username(self):
        payload = self._create_message('invalid_username', self.password, 'Order', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Invalid authorisation', response.text)

    def test_invalid_password(self):
        payload = self._create_message(self.username, 'invalid_password', 'Order', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Invalid authorisation', response.text)

    def test_invalid_username_password(self):
        payload = self._create_message('invalid_username', 'invalid_password', 'Order', self.packet).encode('utf-8')
        response = requests.request('POST', self.url, data=payload, headers=self.headers)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Invalid authorisation', response.text)

    @staticmethod
    def _create_message(username, password, action, packet):
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

    @staticmethod
    def _get_packet():
        with open('./test/files/lixi/valid_message.xml', 'r') as file:
            packet = file.read()
        return packet
