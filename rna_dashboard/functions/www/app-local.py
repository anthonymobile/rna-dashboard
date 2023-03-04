# this local debug version of the app.py file imports the folium map function
# and loads the static content from the local files not S3

# Start the flask server by running:
# python flask_example.py
# head to http://127.0.0.1:5000/ in your browser to see the map displayed
# thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

from flask import Flask

import boto3
from app import fullscreen_map

#this should mimic the behavior of the production app
app = Flask(__name__,
            static_url_path='/static', 
            static_folder='../../data/www'
)

# Initialize the S3 client
s3 = boto3.client('s3')



@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()


#### DEBUG ###############################################################################
# We only need this for local execution.

if __name__ == "__main__":
    app.run(debug=True)
