from pymongo import MongoClient
from flask import Flask, jsonify
from sqlalchemy.ext.declarative import declarative_base




app = Flask(__name__)  

Base = declarative_base()



### For MongoDB Atlas Connection###
mongodb_uri =  "mongodb+srv://fusemachines:hello123@cluster0.q8imdqk.mongodb.net/?retryWrites=true&w=majority"

### For MogoDB localhost connection ###
# mongodb_uri = "mongodb://localhost:27017"

client = MongoClient(mongodb_uri)
for db_name in client.list_database_names():
         print(db_name)



@app.route('/',methods = ['GET'])
def home():
    mydb = client['fusemachines_db']
    collection  = mydb["users"]
    x = collection.find_one()
    response_data =[]

    for x,y in collection.find():
        print(x)
        # data_dict = dict()
        # data_dict['x.name'] = x.name
        response_data.append(x)
    print(type(x))
    return jsonify(
            {
                'status': response_data.name
            }
        )


if __name__ == '__main__':
    app.run(debug=True)