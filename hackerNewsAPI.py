import requests

class HackerNewsAPI(object):
  def __init__(self,topNum):
    self.topNum=topNum
    
  def topStories(self):
    """Request top stories from Hacker News API
    """
    r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')    
    return [ i for i in r.json()[:self.topNum] ]

  def item(self,id):    
    """Request item from Hacker News API
    """
    return requests.get('https://hacker-news.firebaseio.com/v0/item/'+str(id)+'.json').json()