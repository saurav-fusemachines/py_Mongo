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
    


#INSERT MANY
@app.route("/add_many",methods= ['POST'])
def add_many():
    body = request.get_json()
    db.users.insert_many(
     body
        )
    return flask.jsonify(message="success",data_inserted=json.loads(json_util.dumps(body)))



#UPDATE AND REPLACE DOCUMENT
'''replace_one() has the following arguments:

filter - A query which defines which entries will be replaced.
replacement - Entries that will be put in their place when replaced.
{} - A configuration object which has a few options, of which well be focusing on - upsert.'''

#UPDATE AND REPLACE
@app.route("/replace_name/<int:userID>", methods = ['POST'])
def replace_one(userID):
    body = request.get_json()
    result = db.users.replace_one({'eid': userID}, body)
    return {'id': result.raw_result}


#UPDATE AND SET
@app.route("/update_name/<int:userID>", methods = ['POST'])
def update_one(userID):
    body = request.get_json()
    result = db.users.update_one({'eid': userID}, body)
    return result.raw_result


#DELETING DOCUMENT
@app.route("/delete_user/<int:userID>", methods=['DELETE'])
def delete_user(userID):
    user = db.users.delete_one({'eid': userID})
    # return user.raw_result
    return flask.jsonify(message="success",data_deleted=json.loads(json_util.dumps(user.raw_result)))


#USING COMPARATORS
@app.route("/lt", methods=['GET'])
def lessthan():
    salaries = db.salaries.find({'salary': {'$lt':500000}})
    return flask.jsonify(message="success",data=json.loads(json_util.dumps(salaries)))

if __name__ == '__main__':
    app.run(debug=True)

