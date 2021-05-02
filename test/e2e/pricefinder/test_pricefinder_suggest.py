import requests
import json
from unittest import TestCase

from test import config


class TestPriceFinderSuggest(TestCase):

    def setUp(self):
        self.url = f'{config.hostname()}/pricefinder/v1/suggest'

    def test_should_return_search_suggestion(self):
        response = requests.get(self.url, params={
            'q': '20 SOMERVILLE STREET'
        }, headers={
            'authorization': 'Bearer token'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.text)
        self.assertGreater(len(data['matches']), 0)

    def test_should_return_no_search_suggestion(self):
        response = requests.get(self.url, headers={
            'authorization': 'Bearer token'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.text)
        self.assertEqual(len(data['matches']), 0)

    def test_should_return_unauthorized_request_with_no_authorization_header(self):
        response = requests.get(self.url, params={
            'q': '20 SOMERVILLE STREET'
        })
        self.assertEqual(response.status_code, 401)

    def test_should_return_unauthorized_request_with_an_invalid_token(self):
        response = requests.get(self.url, params={
            'q': '20 SOMERVILLE STREET'
        }, headers={
            'authorization': 'invalid token'
        })
        self.assertEqual(response.status_code, 401)

    def test_should_only_allow_get_requests(self):
        for action_method in ['POST', 'PUT', 'DELETE']:
            response = requests.request(action_method, self.url, params={
                'q': '20 SOMERVILLE STREET'
            }, headers={
                'authorization': 'invalid token'
            })
            self.assertEqual(response.status_code, 405)
