from flask import *
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from hackernews_api import HackerNewsAPI
from unbabel_api import UnbabelAPI
from manager_db import DatabaseManager

TOP_STORIES = 10
UNBABEL_USER = "backendchallenge"
UNBABEL_APIKEY = "d1d01e730f33285c89424412088fed716efdb7e7"
LANGUAGES_LIST = ['es', 'pt']
#UPDATE_RATE = 10 #keeping this site updated with hackernews every X minutes
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

# Initialize mongodb
mongo = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo['unbabel_challenge']
collection = db['collection']

hackernews = HackerNewsAPI(TOP_STORIES)
unbabel = UnbabelAPI(UNBABEL_USER,UNBABEL_APIKEY)
manager = DatabaseManager(collection, hackernews, unbabel, LANGUAGES_LIST)

#APScheduler stuff!!
def update_top_stories():
    manager.update_top_stories()


def update_a_random_pt_translation():
    manager.update_a_translation('pt')


def update_a_random_es_translation():
    manager.update_a_translation('es')

scheduler = BackgroundScheduler()
#job = scheduler.add_job(update_top_stories, 'interval', UPDATE_RATE)
job = scheduler.add_job(update_top_stories, 'interval', seconds=30000)
job = scheduler.add_job(update_a_random_pt_translation, 'interval', seconds=3000)
job = scheduler.add_job(update_a_random_es_translation, 'interval', seconds=3000)

#Flask stuff!!
app = Flask(__name__, static_url_path='')

@app.route('/')
def index():  
    return app.send_static_file('index.html')


@app.route('/topstories.json', methods=['GET'])
def topStories():
    cursor = collection.find_one({'tops' : {'$exists' : 'true'}})
    return jsonify(cursor['tops'])


@app.route('/item/<id_>.json', methods=['GET'])
def item(id_):
    cursor = collection.find_one({'id' : int(id_),'type' : 'story'})
    del cursor['_id']
    return jsonify(cursor)


@app.route('/translation/<id_>_<target_language>/', methods=['GET'])
def translation(id_, target_language):
    cursor = collection.find_one({'id' : int(id_), 'target_language' : target_language})
    del cursor['_id']
    return jsonify(cursor)

# Start running the flask app
if __name__ == '__main__': 
    manager.start()
    scheduler.start()  
    app.run(debug=True,port=5000)
