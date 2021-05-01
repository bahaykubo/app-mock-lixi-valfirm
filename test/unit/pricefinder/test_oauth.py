from django.test import TestCase
import json


class TestPricefinderOauth(TestCase):

    def setUp(self):
        self.path = '/pricefinder/v1/oauth2/token'

    def test_should_return_access_token_on_valid_authorization_request(self):
        response = self.client.post(self.path, data={
            'grant_type': 'bong',
            'client_id': 'bing',
            'client_secret': 'bong',
        })
        assert response.status_code == 200

        data = json.loads(response.content)
        assert data['access_token']

    def test_should_return_unauthorized_on_missing_client_id(self):
        response = self.client.post(self.path, data={
            'grant_type': 'bong',
            'client_secret': 'bong',
        })
        assert response.status_code == 400

    def test_should_return_unauthorized_on_missing_client_secret(self):
        response = self.client.post(self.path, data={
            'grant_type': 'bong',
            'client_id': 'bing',
        })
        assert response.status_code == 400

    def test_should_return_unauthorized_on_missing_client_id_and_secret(self):
        response = self.client.post(self.path, data={
            'grant_type': 'bong',
        })
        assert response.status_code == 400
