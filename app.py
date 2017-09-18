from flask import *
from pymongo import MongoClient
from unbabel.api import UnbabelApi
from apscheduler.scheduler import Scheduler
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

sched = Scheduler()
sched.start()

# Schedule job_function to be called every x seconds
@sched.interval_schedule(seconds=30)
def job_function():
    dbHelper.updateCollection()


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