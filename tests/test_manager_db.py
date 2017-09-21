from unittest import TestCase
from mock import Mock, patch
from manager_db import DatabaseManager

class Test_DatabaseManager(TestCase):

    def test_update_top_stories(self):
        database = Mock()
        hackernews = Mock()
        unbabel = Mock()
        languages = Mock()
        manager=DatabaseManager(database, hackernews, unbabel, languages)

        hackernews.get_top_stories.return_value=[1,2,3]
        manager.update_top_stories()
        self.assertEqual(manager.top_stories,[1,2,3])

        hackernews.get_top_stories.return_value=[1,4,3]
        manager.update_top_stories()
        self.assertEqual(manager.top_stories,[1,4,3])
    
    def test_update_a_translation(self):
        database = Mock()
        hackernews = Mock()
        unbabel = Mock()
        languages = Mock()
        manager=DatabaseManager(database, hackernews, unbabel, languages)

        database.find_one.return_value = {
            'status': 'new',
            'uid': 'ac1a53a264',
            'id': 4
        }
        new_trans_status = unbabel.get_translation.return_value = {
            'status': 'translating',
            'uid': 'ac1a53a264'
        }
        manager.update_a_translation('fake')

        self.assertIn('id', new_trans_status)
