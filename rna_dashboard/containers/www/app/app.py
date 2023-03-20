from flask import Flask, send_from_directory
import serverless_wsgi

from Map import fullscreen_map

import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

# bucket_url=os.getenv('BUCKET_URL')
bucket_url="data/www/maps"


@app.route('/maps/<path:path>')
def map_layers(path): 
    return send_from_directory(
        'maps', 
        path, 
        mimetype='application/json'
        )

@app.route("/")
def homepage():
    return fullscreen_map(bucket_url).get_root().render()

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
