from flask import Flask, request, send_from_directory

from Map import fullscreen_map

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
# https://arunkprasad.com/log/how-to-create-a-static-website-with-flask/


from flask_frozen import Freezer

app.debug = False
freezer = Freezer(app)

# By default, `freezer` writes to the `build` directory
freezer.freeze()


@app.route("/")
def homepage():
    return fullscreen_map(request.base_url).get_root().render()
