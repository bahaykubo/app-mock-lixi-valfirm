from unittest import TestCase
import requests
import json

from test import config


class TestPriceFinderImages(TestCase):

    def setUp(self):
        self.url = f'{config.hostname()}/pricefinder/v1/images'

    def test_should_return_an_image_given_an_image_id_in_number(self):
        response = requests.get(f'{self.url}/907', headers={
            'authorization': 'Bearer sometoken'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('image', response.headers['content-type'])

    def test_should_return_an_error_given_an_image_id_not_number(self):
        response = requests.get(f'{self.url}/xyz', headers={
            'authorization': 'Bearer sometoken'
        })
        self.assertEqual(response.status_code, 404)

    def test_should_return_an_error_given_no_image_id(self):
        response = requests.get(f'{self.url}', headers={
            'authorization': 'Bearer sometoken'
        })
        self.assertEqual(response.status_code, 404)

    def test_should_return_unauthorized_request_with_no_authorization_header(self):
        response = requests.get(f'{self.url}/907')
        self.assertEqual(response.status_code, 401)

    def test_should_return_unauthorized_request_with_an_invalid_token(self):
        response = requests.get(f'{self.url}/907', headers={
            'authorization': 'invalid token'
        })
        self.assertEqual(response.status_code, 401)

    def test_should_only_allow_get_requests(self):
        for action_method in ['POST', 'PUT', 'DELETE']:
            response = requests.request(action_method, f'{self.url}/907', headers={
                'authorization': 'Bearer token'
            })
            self.assertEqual(response.status_code, 405)
