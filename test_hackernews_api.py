from unittest import TestCase
from mock import Mock, patch
from hackernews_api import HackerNewsAPI
from requests import get

class TestHackerNewsAPI(TestCase):
    def test_get_top_stories(self):
        hackernews = HackerNewsAPI(0)
        self.assertEqual(len(hackernews.get_top_stories()), 0)

        hackernews = HackerNewsAPI(5)
        self.assertEqual(len(hackernews.get_top_stories()), 5)

        hackernews = HackerNewsAPI(550)
        self.assertLessEqual(len(hackernews.get_top_stories()), 500)

    def test_get_item(self):
        with patch('hackernews_api.get') as fake_get:
            hackernews = HackerNewsAPI(0)
            
            fake_get.return_value.status_code = 200
            result = hackernews.get_item(0)            
            self.assertIsNotNone(result)

            fake_get.return_value.status_code = 404
            result = hackernews.get_item(0)            
            self.assertIsNone(result)