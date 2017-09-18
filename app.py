from flask import *
from pymongo import MongoClient
from unbabel.api import UnbabelApi
from make_celery import *
from hackerNewsAPI import HackerNewsAPI
from dbHelper import DbHelper

# Initialize flask app
app = Flask(__name__,static_url_path='')

# Initialize mongodb
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
mongo = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo['unbabel_challenge']
collection = db['collection']

# Class to help inicialize and update the db
dbHelper=DbHelper(10,collection)
dbHelper.initCollection()

# Initialize celery
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

#add periodic task to celery
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #calls updater() every 30 seconds.
    sender.add_periodic_task(30.0, updater.s())


@celery.task(name='app.updater')
def updater():
    return dbHelper.updateCollection()

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