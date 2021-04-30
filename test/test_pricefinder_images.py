import unittest
import requests
import json

from mock_service.pricefinder.v1 import views


class TestPriceFinderImages(unittest.TestCase):

    def setUp(self):
        self.url = 'http://lixi-mock-valfirm-service.azurewebsites.net/pricefinder/v1/images'

    def test_should_return_random_id_if_outside_900_907_range(self):
        random_id = views._image_id_selector('900001')
        assert random_id

    def test_should_return_none_if_in_900_907_range(self):
        random_id = views._image_id_selector('905')
        assert random_id is None

    def test_should_return_an_image_given_an_image_id_in_number(self):
        response = requests.get(f'{self.url}/907', headers={
            'authorization': 'Bearer sometoken'
        })
        assert response.status_code == 200
        assert 'image' in response.headers['content-type']

    def test_should_return_an_error_given_an_image_id_not_number(self):
        response = requests.get(f'{self.url}/xyz', headers={
            'authorization': 'Bearer sometoken'
        })
        assert response.status_code == 404

    def test_should_return_an_error_given_no_image_id(self):
        response = requests.get(f'{self.url}', headers={
            'authorization': 'Bearer sometoken'
        })
        assert response.status_code == 404

    def test_should_return_unauthorized_request_with_no_authorization_header(self):
        response = requests.get(f'{self.url}/907')
        assert response.status_code == 401

    def test_should_return_unauthorized_request_with_an_invalid_token(self):
        response = requests.get(f'{self.url}/907', headers={
            'authorization': 'invalid token'
        })
        assert response.status_code == 401

    def test_should_only_allow_get_requests(self):
        for action_method in ['POST', 'PUT', 'DELETE']:
            response = requests.request(action_method, f'{self.url}/907', headers={
                'authorization': 'Bearer token'
            })
            assert response.status_code == 405
