from unittest import TestCase
import requests
import json

from test import config


class TestLendfast(TestCase):

    def setUp(self):
        self.hostname = config.hostname()
        self.url = f'{self.hostname}/mocklender/notify'
        self.headers = {'content-type': 'application/xml'}
        self.token_url = f'{self.hostname}/as/token.oauth2'
        self.token_headers = {'content-type': 'application/x-www-form-urlencoded'}

        self.packet = '<q1:notificationList xmlns:q1="http://www.sandstone-vms.com.au/schema/vms/1.0"><q1:notification type="StatusChange" timestamp="2020-05-29T12:57:27.2581866"><Identifier UniqueID="cf456220-cc3a-4dfd-8ddd-7714dfec69f1" Description="Notification ID" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction" /><Identifier UniqueID="LCA-ET4R-RET" Description="Valuation ID" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction" /><Status Name="Accepted" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction"><Date>2020-05-29</Date><Time>12:57:00.0000000+10:00</Time></Status></q1:notification></q1:notificationList>'

        self.invalid_packet = '<q1:XnotificationList xmlns:q1="http://www.sandstone-vms.com.au/schema/vms/1.0"><q1:notification type="StatusChange" timestamp="2020-05-29T12:57:27.2581866"><Identifier UniqueID="cf456220-cc3a-4dfd-8ddd-7714dfec69f1" Description="Notification ID" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction" /><Status Name="Accepted" xmlns="http://www.lixi.org.au/schema/cal1.3/ValuationTransaction"></Status></q1:notification></q1:XnotificationList>'

    def test_oath2_returns_token(self):
        response = requests.post(self.token_url, headers=self.token_headers)
        self.assertEqual(response.status_code, 200)
        token = json.loads(response.text)
        self.assertIsNotNone(token['access_token'])

    def test_oath2_only_put_method_allowed(self):
        methods = ['GET', 'PUT', 'DELETE']
        for method in methods:
            response = requests.request(method, self.token_url, headers=self.token_headers)
            self.assertEqual(response.status_code, 405)

    def test_lender_successful_soap_message(self):
        response = requests.post(self.url, data=self.packet, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('acknowledge', response.text)

    def test_only_put_method_allowed(self):
        methods = ['GET', 'PUT', 'DELETE']
        for method in methods:
            response = requests.request(method, self.url, data=self.packet, headers=self.headers)
            self.assertEqual(response.status_code, 400)

    def test_invalid_message(self):
        invalid_packet = '<xml>invalid</xml>'
        response = requests.post(self.url, data=invalid_packet, headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.text)

    def test_invalid_soap_action_method(self):
        response = requests.post(self.url, data=self.invalid_packet, headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.text)
