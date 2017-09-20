from requests import get, post
from flask import jsonify

class UnbabelAPI(object):
    """
    Class to interact with Unbabel API
    """
    base_url = 'https://api.unbabel.com/tapi/v2/translation/'

    def __init__(self, user, apikey):
        self.headers = {
            'Authorization': 'ApiKey {}:{}'.format(user, apikey),
            'Content-Type': 'application/json'
        }

    def request_translation(self, text, language): 
        data = {
            'text': text,
            'text_format': 'html',
            'target_language': language
        }
        uid = post(self.base_url, headers=self.headers, data=data)   
        
        if uid and uid.status_code == 201:
            return uid.json()
        return None

    def get_translation(self, uid):
        url = '{}{}/'.format(self.base_url, uid)
        translation = get(url, headers=self.headers)

        if translation and translation.status_code == 200:
            return translation.json()
        return None
    