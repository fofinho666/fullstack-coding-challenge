from requests import get, post
import json

class UnbabelAPI(object):
    """
    Class to interact with Unbabel API
    """
    base_url = 'https://sandbox.unbabel.com/tapi/v2/translation/'

    def __init__(self, user, apikey):
        self.headers = {
            'Authorization' : 'ApiKey {}:{}'.format(user, apikey),
            'Content-Type' : 'application/json'
        }
    def request_translation(self, text, language):        
        try:
            data = {
                'text': text,
                'target_language': language,
                'text_format': 'text'
            }
            uid = post(self.base_url, headers=self.headers, data=json.dumps(data))
            
            if uid and uid.status_code == 201:
                return uid.json()
            return None
        except:
            return None

    def get_translation(self, uid):        
        try:
            url = '{}{}/'.format(self.base_url, uid)
            translation = get(url, headers=self.headers)

            if translation and translation.status_code == 200:
                return translation.json()
            return None
        except:
            return None
    