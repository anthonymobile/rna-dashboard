# this production version is deployed to AWS Lambda via the Serverless Framework

import json
from flask import Flask, Response, send_file
import serverless_wsgi

from Map import fullscreen_map

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
# app = Flask(__name__,
#             static_folder="maps", 
#             static_url_path="/maps")

@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()

# @app.route('/maps/<path:path>')
# def map_layers(path):
#     return send_file(f"maps/{path}", mimetype="application/json")

#TODO this feels really cumbersome, can't we just read the file instead of converting it to a dict and then back to a string?
@app.route('/maps/<path:path>')
def map_layers(path):
    
    with app.open_resource(f"maps/{path}") as f:     
        data = json.load(f)

    return Response(json.dumps(data), mimetype='application/json')



def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
