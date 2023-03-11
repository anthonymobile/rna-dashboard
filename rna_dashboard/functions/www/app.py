# this production version is deployed to AWS Lambda via the Serverless Framework

from flask import Flask, send_file
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

@app.route('/maps/<path:path>')
def map_layers(path):
    return send_file(f"maps/{path}", mimetype="application/json")


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
