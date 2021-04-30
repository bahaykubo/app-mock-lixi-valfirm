import unittest
import requests
import json


class TestPriceFinderSuggest(unittest.TestCase):

    def setUp(self):
        self.url = 'https://lixi-mock-valfirm-service.azurewebsites.net/pricefinder/v1/suggest'

    def test_should_return_search_suggestion(self):
        response = requests.get(self.url, params={
            'q': '20 SOMERVILLE STREET'
        }, headers={
            'authorization': 'Bearer token'
        })
        assert response.status_code == 200

        data = json.loads(response.text)
        assert len(data['matches']) > 0

    def test_should_return_no_search_suggestion(self):
        response = requests.get(self.url, headers={
            'authorization': 'Bearer token'
        })
        assert response.status_code == 200

        data = json.loads(response.text)
        assert len(data['matches']) == 0

    def test_should_return_unauthorized_request_with_no_authorization_header(self):
        response = requests.get(self.url, params={
            'q': '20 SOMERVILLE STREET'
        })
        assert response.status_code == 401

    def test_should_return_unauthorized_request_with_an_invalid_token(self):
        response = requests.get(self.url, params={
            'q': '20 SOMERVILLE STREET'
        }, headers={
            'authorization': 'invalid token'
        })
        assert response.status_code == 401

    def test_should_only_allow_get_requests(self):
        for action_method in ['POST', 'PUT', 'DELETE']:
            response = requests.request(action_method, self.url, params={
                'q': '20 SOMERVILLE STREET'
            }, headers={
                'authorization': 'invalid token'
            })
            assert response.status_code == 405
