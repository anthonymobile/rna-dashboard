from flask import Flask, request, send_from_directory
from flask_frozen import Freezer

from Map import fullscreen_map

app = Flask(__name__)
app.config['FREEZER_BASE_URL'] = 'http://localhost:5000'
app.config['FREEZER_DESTINATION'] = 'build'
freezer = Freezer(app)

@app.cli.command()
def freeze():
    freezer.freeze()

@app.route("/")
def homepage():
    return fullscreen_map(request.base_url).get_root().render()
