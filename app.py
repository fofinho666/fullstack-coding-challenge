from flask import *
from pymongo import MongoClient
from apscheduler.scheduler import Scheduler
from hackernews_api import HackerNewsAPI
from unbabel_api import UnbabelAPI
from manager_db import DatabaseManager

TOP_STORIES = 10
UNBABEL_USER = "backendchallenge"
UNBABEL_APIKEY = "711b8090e84dcb4981e6381b59757ac5c75ebb26"
LANGUAGES_LIST = ['es', 'pt']
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

# Initialize flask app
app = Flask(__name__,static_url_path='')

# Initialize mongodb
mongo = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo['unbabel_challenge']
collection = db['collection']

hackernews = HackerNewsAPI(TOP_STORIES)
unbabel = UnbabelAPI(UNBABEL_USER,UNBABEL_APIKEY)
manager = DatabaseManager(collection, hackernews, unbabel, LANGUAGES_LIST)

sched = Scheduler()
sched.start()
# Schedule job_function to be called every x seconds
@sched.interval_schedule(seconds=30)
def update_top_stories():
    manager.update_top_stories()
    
@sched.interval_schedule(seconds=1)
def update_a_random_pt_translation():
    manager.update_a_random_translation('pt')
    
@sched.interval_schedule(seconds=1)
def update_a_random_es_translation():
    manager.update_a_random_translation('es')

#flask stuff!!
@app.route('/')
def index():  
    return app.send_static_file('index.html')


@app.route('/topstories.json',methods=['GET'])
def topStories():
    cursor = collection.find_one({ 'tops' : { '$exists' : 'true' } })
    return jsonify(cursor['tops'])


@app.route('/item/<id>.json',methods=['GET'])
def item(id):
    cursor = collection.find_one({ 'id' : int(id) })
    del cursor['_id']
    return jsonify(cursor)


# Start running the flask app
app.debug = True

if __name__ == '__main__':
	app.run()