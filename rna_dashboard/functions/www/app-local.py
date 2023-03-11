# this local debug version of the app.py file imports the folium map function
# and loads the maps content from the local files not S3

# Start the flask server by running:
# python flask_example.py
# head to http://127.0.0.1:5000/ in your browser to see the map displayed
# thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

# import os
from flask import Flask #, send_file

import boto3
from app import fullscreen_map

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#this should mimic the behavior of the production app
app = Flask(__name__,
            static_folder="maps", 
            static_url_path="/maps")


@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()


#### DEBUG ###############################################################################
# We only need this for local execution.

if __name__ == "__main__":
    app.run(debug=True)
