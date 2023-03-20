from flask import Flask, request, send_from_directory

from Map import fullscreen_map

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/")
def homepage():
    return fullscreen_map(request.base_url).get_root().render()
