from unittest import TestCase
import requests
import json

from test import config


class TestPriceFinderPropertiesImages(TestCase):

    def setUp(self):
        self.url = f'{config.hostname()}/pricefinder/v1/properties'

    def test_should_return_list_of_property_images_given_a_property_id_number(self):
        response = requests.get(f'{self.url}/900/images', headers={
            'authorization': 'Bearer token'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.text)
        assert len(data['images']) > 0

        for image in data['images']:
            self.assertIn('_self', image)
            self.assertIn('http', image['_self'])

    def test_should_return_an_error_given_a_property_id_not_number(self):
        response = requests.get(f'{self.url}/xyz/images', headers={
            'authorization': 'Bearer token'
        })
        self.assertEqual(response.status_code, 404)

    def test_should_return_unauthorized_request_with_no_authorization_header(self):
        response = requests.get(f'{self.url}/900/images')
        self.assertEqual(response.status_code, 401)

    def test_should_return_unauthorized_request_with_an_invalid_token(self):
        response = requests.get(f'{self.url}/900/images', headers={
            'authorization': 'invalid token'
        })
        self.assertEqual(response.status_code, 401)

    def test_should_only_allow_get_requests(self):
        for action_method in ['POST', 'PUT', 'DELETE']:
            response = requests.request(action_method, f'{self.url}/900/images', headers={
                'authorization': 'Bearer token'
            })
            self.assertEqual(response.status_code, 405)
