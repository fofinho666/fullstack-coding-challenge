from unittest import TestCase
from mock import Mock, patch
from unbabel_api import UnbabelAPI
from requests import get, post

class TestUnbabelAPI(TestCase):
    def test_request_translation(self): 
        with patch('unbabel_api.post') as fake_post:
            unbabel = UnbabelAPI('user', 'key')

            fake_post.return_value.status_code = 201
            result = unbabel.request_translation('text', 'language')
            self.assertIsNotNone(result)

            fake_post.return_value.status_code = 400
            result = unbabel.request_translation('text', 'language')                      
            self.assertIsNone(result)

    def test_get_translation(self):
        with patch('unbabel_api.get') as fake_get:
            unbabel = UnbabelAPI('user', 'key')

            fake_get.return_value.status_code = 200
            result = unbabel.get_translation(0)
            self.assertIsNotNone(result)

            fake_get.return_value.status_code = 400
            result = unbabel.get_translation(0)                     
            self.assertIsNone(result)
    