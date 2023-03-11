# Start the flask server by running:
# python flask_example.py
# head to http://127.0.0.1:5000/ in your browser to see the map displayed

from flask import Flask
from app import fullscreen_map

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__,
            static_folder="maps", 
            static_url_path="/maps")

@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()

if __name__ == "__main__":
    app.run(debug=True)
