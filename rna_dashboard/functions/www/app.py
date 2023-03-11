# this production version is deployed to AWS Lambda via the Serverless Framework

from flask import Flask
import serverless_wsgi

from Map import fullscreen_map

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__,
            static_folder="maps", 
            static_url_path="/maps")

@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
