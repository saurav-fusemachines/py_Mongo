from flask_pymongo import PyMongo
import flask
from bson import json_util
from pymongo import MongoClient
import requests,json
from flask import request, jsonify

app = flask.Flask(__name__)

mongodb_client = PyMongo(app,uri="mongodb://localhost:27017/fusedb")

db = mongodb_client.db

app.config["MONGO_URI"] = "mongodb://localhost:27017/fusedb"
mongodb_client = PyMongo(app)
db = mongodb_client.db

#READ DOCUMENT
@app.route("/", methods = ['GET'])
def home():
    users = db.users.find()
    # return flask.jsonify(json.loads([user for user in users]))
    return json.loads(json_util.dumps(users))


#GET DOCUMENT BY ID    
@app.route("/get_user/<int:userID>",methods = ['GET'])
def getbyID(userID):
    users = db.users.find_one({"eid":userID})
    return flask.jsonify(message="success",data=json.loads(json_util.dumps(users)))


# INSERT ONE
@app.route("/add_one",methods = ['POST'])
def add_one():
    body = request.get_json()
    # db.users.insert_one({'name': "Saurarv Karki", 'email': "saurav.karki@fusemachines.com"})
    db.users.insert_one(body)
    return flask.jsonify(message="success",data=json.loads(json_util.dumps(body)))


if __name__ == '__main__':
    app.run(debug=True)
