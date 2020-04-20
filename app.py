from flask import Response, Flask, render_template, request,redirect,url_for
import re, pprint, json
from bson.json_util import dumps
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Definitions to set in Dockerfile
# MONGO_URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.stacks

required_params = ["env", "name", "version"]
expected_create_body = "Expected minimal body : \n{\"env\": \"dev\", \"name\":\"app_name\", \"version\" : \"0.0.1\"}"

VERSION_REGEX_PATTERN = "^[0-9]+\.[0-9]+\.[0-9]+[+0-9A-Za-z-]*$"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.form:
        env = request.form['environment']
    else: 
        env = 'dev'
    response = findAllEntriesForEnv(env)
    return render_template('index.html', data=response, envs=db.list_collection_names(), selected_env=env)

@app.route("/list/<env>")
def list (env):
    response = findAllEntriesForEnv(env)
    return Response(response, status=200, mimetype='application/json')


@app.route("/create", methods=['POST'])
def createVersion ():
    # Params check
    if not request.data:
        return Response(expected_create_body, status=400, mimetype='application/json')
    json_payload = json.loads(request.data)

    # Securing payload
    if len(json_payload) > 10: # TODO : Check what value to put here
        return Response("Too many elements in payload", status=400, mimetype='application/json')
    for key in json_payload:
        if key.find("$") != -1 or json_payload[key].find("$") != -1: # In order to avoid noasql or script injection
            print(json_payload[key])
            return Response('"$" character not allowed in "'+key+'":"'+json_payload[key]+'"', status=400, mimetype='application/json')

    # Validating presence of params
    for param in required_params:
        if not param in json_payload: # checks if param exists
            return Response("Missing param : "+param+"\n"+expected_create_body, status=400, mimetype='application/json')
        if not json_payload[param]: # checks if param is empty
            return Response("Param '"+param+"' can't be empty \n"+expected_create_body, status=400, mimetype='application/json')

    # Assigning mandatory params to values
    env = json_payload['env']
    name = json_payload['name']
    version = json_payload['version']

    for el in json_payload:
        print(el)

    if not re.search(VERSION_REGEX_PATTERN, version):
        print("Version does not match regex")
        # Here return error invalid param
        return Response("Version must match following regex : "+VERSION_REGEX_PATTERN, status=400, mimetype='application/json')
        
    else: # version matches regex
        available_collections = db.list_collection_names()
        if env not in available_collections:
            print("Couldn't find '"+env+"' in "+str(available_collections))
        
        stack = db[env] # Selecting the collection from request
        counted_results = stack.count_documents({"name": {"$regex" : "^" + name + "$"}})

        if counted_results > 1 :
            return Response("More than one application with the name : " + name, status=409, mimetype='application/json')
            
        elif counted_results < 1 : # no entry, so we create
            json_payload['date'] = datetime.now()
            stack.insert_one(json_payload) # all the mandatory values seem to be ok so we can insert
            return Response("Creation successful", status=200, mimetype='application/json')

        else: # exactly one entry, so we update
            json_payload['date'] = datetime.now()
            stack.update_one({"name": name}, { "$set" : json_payload})
            return Response("Update successful", status=200, mimetype='application/json')
    
    return Response("Unexpected error", status=418, mimetype='application/json')


def findAllEntriesForEnv(env):
    stack = db[env]
    return dumps(stack.find())



if __name__ == "__main__":
    app.run()