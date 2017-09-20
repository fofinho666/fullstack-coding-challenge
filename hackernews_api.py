from requests import get

class HackerNewsAPI(object):
    """
    Class to interact with Hacker News API
    """
    base_url = 'https://hacker-news.firebaseio.com/v0/'

    def __init__(self, top_num):
        self.top_num = top_num

    def get_top_stories(self):
        try:
            url = '{}/topstories.json'.format(self.base_url)
            ids = get(url)
            
            if ids and ids.status_code == 200:
                return [id_ for id_ in ids.json()[:self.top_num]]
            return []
        except:
            return []

    def get_item(self, id_):
        try:
            url = '{}item/{}.json'.format(self.base_url, id_)
            item = get(url)
            
            if item and item.status_code == 200:
                return  item.json()
            return None
        except:
            return None
