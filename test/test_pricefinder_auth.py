import unittest
import requests
import json


class TestPriceFinderAuth(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/pricefinder/v1/oauth2/token'

    def test_should_return_access_token_on_valid_authorization_request(self):
        response = requests.post(self.url, data={
            'grant_type': 'bong',
            'client_id': 'bing',
            'client_secret': 'bong',
        }, headers={
            'content-type': 'application/x-www-form-urlencoded'
        })
        assert response.status_code == 200

        data = json.loads(response.text)
        assert data['access_token']

    def test_should_return_unauthorized_on_missing_client_id(self):
        response = requests.post(self.url, data={
            'grant_type': 'bong',
            'client_secret': 'bong',
        }, headers={
            'content-type': 'application/x-www-form-urlencoded'
        })
        assert response.status_code == 400

    def test_should_return_unauthorized_on_missing_client_secret(self):
        response = requests.post(self.url, data={
            'grant_type': 'bong',
            'client_id': 'bing',
        }, headers={
            'content-type': 'application/x-www-form-urlencoded'
        })
        assert response.status_code == 400

    def test_should_return_unauthorized_on_missing_client_id_and_secret(self):
        response = requests.post(self.url, data={
            'grant_type': 'bong',
        }, headers={
            'content-type': 'application/x-www-form-urlencoded'
        })
        assert response.status_code == 400

    def test_should_only_allow_post_requests(self):
        for action_method in ['GET', 'PUT', 'DELETE']:
            response = requests.request(action_method, self.url, data={
                'grant_type': 'bong',
                'client_id': 'bing',
                'client_secret': 'bong',
            }, headers={
                'content-type': 'application/x-www-form-urlencoded'
            })
            assert response.status_code == 405
