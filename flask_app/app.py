from flask import Response, Flask, render_template, request,redirect,url_for
import re, pprint, json
from bson.json_util import dumps
from pymongo import MongoClient
from datetime import datetime
from utils.vars import *
from config import *

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client.stacks

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.form:
        env_collection = request.form['environment']
    else: # default value for collection, needs to be rethinked with empty DB
        available_collections = db.list_collection_names()
        if not available_collections:
            return render_template('index.html')
        env_collection = available_collections[0]
    response = findAllEntriesForEnv(env_collection)
    # Route for template rendering
    return render_template(
        'index.html',
        data=response,
        envs=db.list_collection_names(),
        selected_env=env_collection
    )

@app.route("/list/<env_collection>")
def list (env_collection): # Check characters for security here ?
    response = findAllEntriesForEnv(env_collection)
    return Response(response, status=200, mimetype='application/json')


@app.route("/create", methods=['POST'])
def createVersion ():
    # Payload presence check
    if not request.data:
        return Response(expected_create_body, status=400, mimetype='application/json')
    json_payload = json.loads(request.data)

    # Securing payload
    if len(json_payload) > 10: # TODO : Check what value to put here
        return Response("Too many elements in payload", status=400, mimetype='application/json')
    for key in json_payload:
        if key.find("$") != -1 or key.find(".") != -1: # Mongo-related security, see README.md
            return Response('"$" character not allowed in "'+key+'":"'+json_payload[key]+'"', status=400, mimetype='application/json')
        if json_payload[key].find("<") != -1 or json_payload[key].find(">") != -1 : # To avoid arbitrary html sent to app when showing in template
            return Response('"<" and ">" characters not allowed in "'+key+'":"'+json_payload[key]+'"', status=400, mimetype='application/json')

    # Validating presence of params
    for param in required_params:
        if not param in json_payload: # checks if param exists
            return Response("Missing required param : "+param+"\n"+expected_create_body, status=400, mimetype='application/json')
        if not json_payload[param]: # checks if param is empty
            return Response("Param '"+param+"' can't be empty \n"+expected_create_body, status=400, mimetype='application/json')

    # Assigning mandatory params to values
    env_collection = json_payload['env']
    name = json_payload['name']
    version = json_payload['version']

    # Validating format of version according to https://semver.org
    if not re.search(VERSION_REGEX_PATTERN, version):
        print("Version does not match regex")
        return Response("Version must match following regex : "+VERSION_REGEX_PATTERN, status=400, mimetype='application/json')
    
    # Version matches regex, so we can save the payload in database
    else:
        # Selecting the collection from request
        stack = db[env_collection]

        # Find any application with the same name in the collection
        counted_results = stack.count_documents({"name": {"$regex" : "^" + name + "$"}})

        if counted_results > 1 :
            return Response("More than one application with the name : " + name, status=409, mimetype='application/json')
            
        elif counted_results < 1 : # no entry, so we create
            json_payload['date'] = datetime.now() # add time of creation
            stack.insert_one(json_payload)
            return Response("Creation successful", status=200, mimetype='application/json')

        else: # exactly one entry, so we update
            json_payload['date'] = datetime.now()  # update time of deployement
            stack.update_one({"name": name}, { "$set" : json_payload})
            return Response("Update successful", status=200, mimetype='application/json')
    
    return Response("Unexpected error", status=418, mimetype='application/json')


def findAllEntriesForEnv(env_collection):
    stack = db[env_collection]
    return dumps(stack.find())

if __name__ == "__main__":
    app.run(host='0.0.0.0')