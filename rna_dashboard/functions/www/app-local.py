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

@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()

# # works locally, doesnt work on AWS Lambda
# @app.route('/maps/<path:path>')
# def map_layers(path):
#     return send_file(f"maps/{path}", mimetype="application/json")

# # works locally #TODO test on AWS
# @app.route('/maps/<path:path>')
# def map_layers(path):
    
#     with app.open_resource(f"maps/{path}") as f:     
#         data = json.load(f)

#     return Response(json.dumps(data), mimetype='application/json')

# # works locally #TODO test on AWS
@app.route('/maps/<path:path>')
def map_layers(path):  
    with open(f"maps/{path}") as f: 
        data = f.read()    
        return Response(data, mimetype='application/json')



if __name__ == "__main__":
    app.run(debug=True)