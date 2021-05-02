from django.test import TestCase

from mock_service.pricefinder.v1 import views


class TestPriceFinderImages(TestCase):

    def setUp(self):
        self.path = '/pricefinder/v1/images'
        self.view = views

    def test_should_return_random_id_if_outside_900_907_range(self):
        random_id = self.view._image_id_selector(900001)
        assert random_id

    def test_should_return_none_if_in_900_907_range(self):
        random_id = self.view._image_id_selector(905)
        assert random_id is None

    def test_should_return_none_if_given_a_number_in_string(self):
        random_id = self.view._image_id_selector('905')
        assert random_id is None

    def test_should_return_none_if_given_empty(self):
        random_id = self.view._image_id_selector('')
        assert random_id is None

    def test_should_return_none_if_given_a_string(self):
        random_id = self.view._image_id_selector('a')
        self.assertIsNone(random_id)
