from flask import Response, Flask, render_template, request,redirect,url_for
import re, pprint, json
from bson.json_util import dumps
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.stacks    # Select the database

required_params = ["env", "name", "version"]
expected_list_body = "Expected body : \n{\"env\": \"dev\"}"
expected_create_body = "Expected minimal body : \n{\"env\": \"dev\", \"name\":\"app_name\", \"version\" : \"0.0.1\"}"

VERSION_REGEX_PATTERN = "^[0-9]+\.[0-9]+\.[0-9]+[+0-9A-Za-z-]*$"


@app.route("/list/<env>")
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

    # Assigning params to values
    env = readable_json['env']
    name = readable_json['name']
    version = readable_json['version']

    if not re.search(VERSION_REGEX_PATTERN, version):
        print("Version does not match regex")
        # Here return error invalid param
        return Response("Version must match following regex : "+VERSION_REGEX_PATTERN, status=400, mimetype='application/json')
        
    else: # version matches regex
        stack = db[env] # Selecting the good collection from request
        counted_results = stack.count_documents({"name": {"$regex" : "^" + name + "$"}})

        if counted_results > 1 :
            return Response("More than one application with the name : " + name, status=409, mimetype='application/json')
            
        elif counted_results < 1 : # no entry, so we create
            stack.insert_one({ "name": name, "date": datetime.now() , "version" : version})
            return Response("Creation successful", status=200, mimetype='application/json')

        else: # exactly one entry, so we update
            stack.update_one({"name": name}, { "$set" : readable_json})
            return Response("Update successful", status=200, mimetype='application/json')
    
    return Response("Unknown error", status=418, mimetype='application/json')

if __name__ == "__main__":
    app.run()