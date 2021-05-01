from django.test import TestCase
import json


class TestPricefinderProperties(TestCase):

    def test_image_url(self):
        response = self.client.get('/pricefinder/v1/properties/900', HTTP_AUTHORIZATION='Bearer token')
        self.assertEqual(response.status_code, 200)
