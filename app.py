from flask import Response, Flask, render_template, request,redirect,url_for
import re, pprint, json
from bson.json_util import dumps
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.stacks    # Select the database

required_params = ["env", "name", "version"]
expected_create_body = "Expected minimal body : \n{\"env\": \"dev\", \"name\":\"app_name\", \"version\" : \"0.0.1\"}"

VERSION_REGEX_PATTERN = "^[0-9]+\.[0-9]+\.[0-9]+[+0-9A-Za-z-]*$"


@app.route("/", methods=['GET'])
def index():
    stack = db['dev']
    response = dumps(stack.find({}, {"_id":0}))
    pprint.pprint(response)
    return render_template('index.html', data=response)

@app.route("/list/<env>",  methods=['GET'])
def list (env):
    stack = db[env]
    response = dumps(stack.find())
    return Response(response, status=200, mimetype='application/json')


@app.route("/create", methods=['POST'])
def createVersion ():
    # Params check
    if not request.data:
        return Response(expected_create_body, status=400, mimetype='application/json')
    readable_json = json.loads(request.data)
    for param in required_params:
        if not param in readable_json: # checks if param exists
            return Response("Missing param : "+param+"\n"+expected_create_body, status=400, mimetype='application/json')
        if not readable_json[param]: # checks if param is empty
            return Response("Param '"+param+"' can't be empty \n"+expected_create_body, status=400, mimetype='application/json')

    # Assigning mandatory params to values
    env = readable_json['env']
    name = readable_json['name']
    version = readable_json['version']

    if not re.search(VERSION_REGEX_PATTERN, version):
        print("Version does not match regex")
        # Here return error invalid param
        return Response("Version must match following regex : "+VERSION_REGEX_PATTERN, status=400, mimetype='application/json')
        
    else: # version matches regex
        stack = db[env] # Selecting the good collection from request
        # Check with that if collection exists : db.list_collection_names()
        counted_results = stack.count_documents({"name": {"$regex" : "^" + name + "$"}})

        if counted_results > 1 :
            return Response("More than one application with the name : " + name, status=409, mimetype='application/json')
            
        elif counted_results < 1 : # no entry, so we create
            readable_json['date'] = datetime.now()
            stack.insert_one(readable_json) # all the mandatory values seem to be ok so we can insert
            return Response("Creation successful", status=200, mimetype='application/json')

        else: # exactly one entry, so we update
            readable_json['date'] = datetime.now()
            stack.update_one({"name": name}, { "$set" : readable_json})
            return Response("Update successful", status=200, mimetype='application/json')
    
    return Response("Unexpected error", status=418, mimetype='application/json')

if __name__ == "__main__":
    app.run()