# Start the flask server by running:
# python flask_example.py
# head to http://127.0.0.1:5000/ in your browser to see the map displayed

import json
from flask import Flask, Response, send_file
from app import fullscreen_map

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# app = Flask(__name__,
#             static_folder="maps", 
#             static_url_path="/maps")

app = Flask(__name__)

# METHOD 4
# LOCALLY: WORKS
# AWS: FAILS, files are octet-stream
# map /maps to static
# no special route

# METHOD 5
# LOCALLY: FAILS sends file as octet-stream
# @app.route('/maps/<path:path>')
# def map_layers(path): 
#     return app.send_static_file(path, mimetype="application/json")

# METHOD 6
# LOCALLY: WORKS
# correct content type w/ curl -s -I POST http://127.0.0.1:5000/maps/heights-parcels.geojson
# AWS: #BUG testing on rna6
# OK https://rna6.chilltownlabs.com/maps/boundaries-rna.geojson
# BUG https://rna6.chilltownlabs.com/maps/heights-parcels.geojson
from flask import send_from_directory
@app.route('/maps/<path:path>')
def map_layers(path): 
    return send_from_directory(
        'maps', 
        path, 
        mimetype='application/json'
        )

#FIXME going to have to move the static files somewhere else
#FIXME how about put them in a public S3 bucket, and then use the S3 URL in Map.py 
#FIXME really just need them to be somewhere that we can deploy them with the CDK and then pass the url down into the Map.py class

# METHOD 4
# LOCALLY: #TODO RETEST
# AWS: #TODO test on rna7, app = Flask(__name__)
# @app.route('/maps/<path:path>')
# def map_layers(path):  
#     with open(f"maps/{path}") as f: 
#         data = f.read()    
#         return Response(data, mimetype='application/json')

# METHOD 5
# LOCALLY: #TODO RETEST
# AWS: #TODO test on rna8, app = Flask(__name__)
# # works locally #TODO test on AWS rna8
# @app.route('/maps/<path:path>')
# def map_layers(path):
#     with app.open_resource(f"maps/{path}") as f:     
#         data = json.load(f)
#     return Response(json.dumps(data), mimetype='application/json')

# METHOD 6
# LOCALLY: #TODO RETEST
# AWS: #TODO test on AWS rna9, app = Flask(__name__)
# @app.route('/maps/<path:path>')
# def map_layers(path):
#     return send_file(f"maps/{path}", mimetype="application/json")

@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()

if __name__ == "__main__":
    app.run(debug=True)
