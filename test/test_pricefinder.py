import unittest

from mock_service.pricefinder.v1 import views


class TestPriceFinderImages(unittest.TestCase):

    def test_should_return_random_id_if_outside_900_907_range(self):
        random_id = views._image_id_selector('900001')
        assert random_id

    def test_should_return_none_if_in_900_907_range(self):
        random_id = views._image_id_selector('905')
        assert random_id is None


class TestPriceFinderProperties(unittest.TestCase):
    pass
