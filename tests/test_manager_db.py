from unittest import TestCase  
from mock import Mock, patch
from unbabel_api import UnbabelAPI
from hackernews_api import HackerNewsAPI
import manager_db

class TestDatabaseManager(TestCase):
    def test_add_translation_data_to_title(self):
        fake_item = Mock()
        fake_unbabel = Mock()
        fake_languages = ['fake1', 'fake2']

        fake_item = {}
        result = manager_db.add_translation_data_to_title(fake_item, fake_unbabel, fake_languages)
        self.assertFalse('translation_fake1' in result)
        self.assertFalse('translation_fake2' in result)

        fake_item = {'title' : 'My YC app: Dropbox - Throw away your USB drive'}
        result = manager_db.add_translation_data_to_title(fake_item, fake_unbabel, fake_languages)
        self.assertTrue('translation_fake1' in result)
        self.assertTrue('translation_fake2' in result)

    def test_get_translation_data(self):
        fake_unbabel = Mock()
        
        fake_unbabel.request_translation.return_value = {
            'balance' : 99943.0,
            'client' : 'username',
            'price' : 6.0,
            'source_language' : 'en',
            'status' : 'new',
            'target_language' : 'pt',
            'text' : 'Hello, world!',
            'text_format' : 'text',
            'uid' : 'ac1a53a264'
        }
        result = manager_db.get_translation_data(fake_unbabel, 'text', 'fake')
        self.assertEqual(result['translation_fake_status'], 'translating')

        fake_unbabel.request_translation.return_value = None
        result = manager_db.get_translation_data(fake_unbabel, 'text', 'fake')
        self.assertEqual(result['translation_fake_status'], 'error')
