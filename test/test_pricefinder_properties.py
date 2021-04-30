import unittest
import requests
import json


class TestPriceFinderProperties(unittest.TestCase):

    def setUp(self):
        self.url = 'https://lixi-mock-valfirm-service.azurewebsites.net/pricefinder/v1/properties'

    def test_should_return_property_details_given_a_property_id_number(self):
        response = requests.get(f'{self.url}/900', headers={
            'authorization': 'Bearer token'
        })
        assert response.status_code == 200

        data = json.loads(response.text)
        expected_property_details = ['address', 'features', 'landDetails', 'rpd', 'owners']
        assert all([property_detail in data for property_detail in expected_property_details])

    def test_should_return_error_given_a_property_id_non_number(self):
        response = requests.get(f'{self.url}/xyz', headers={
            'authorization': 'Bearer token'
        })
        assert response.status_code == 404

    def test_should_return_unauthorized_request_with_no_authorization_header(self):
        response = requests.get(f'{self.url}/900')
        assert response.status_code == 401

    def test_should_return_unauthorized_request_with_an_invalid_token(self):
        response = requests.get(f'{self.url}/900', headers={
            'authorization': 'invalid token'
        })
        assert response.status_code == 401

    def test_should_only_allow_get_requests(self):
        for action_method in ['POST', 'PUT', 'DELETE']:
            response = requests.request(action_method, f'{self.url}/900', headers={
                'authorization': 'Bearer token'
            })
            assert response.status_code == 405


class TestPriceFinderPropertiesImages(unittest.TestCase):

    def setUp(self):
        self.url = 'https://lixi-mock-valfirm-service.azurewebsites.net/pricefinder/v1/properties'

    def test_should_return_list_of_property_images_given_a_property_id_number(self):
        response = requests.get(f'{self.url}/900/images', headers={
            'authorization': 'Bearer token'
        })
        assert response.status_code == 200

        data = json.loads(response.text)
        assert len(data['images']) > 0

        for image in data['images']:
            assert '_self' in image and 'http' in image['_self']

    def test_should_return_an_error_given_a_property_id_not_number(self):
        response = requests.get(f'{self.url}/xyz/images', headers={
            'authorization': 'Bearer token'
        })
        assert response.status_code == 404

    def test_should_return_unauthorized_request_with_no_authorization_header(self):
        response = requests.get(f'{self.url}/900/images')
        assert response.status_code == 401

    def test_should_return_unauthorized_request_with_an_invalid_token(self):
        response = requests.get(f'{self.url}/900/images', headers={
            'authorization': 'invalid token'
        })
        assert response.status_code == 401

    def test_should_only_allow_get_requests(self):
        for action_method in ['POST', 'PUT', 'DELETE']:
            response = requests.request(action_method, f'{self.url}/900/images', headers={
                'authorization': 'Bearer token'
            })
            assert response.status_code == 405
