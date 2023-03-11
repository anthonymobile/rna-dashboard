# this production version is deployed to AWS Lambda via the Serverless Framework
# it loads the maps content from S3
# it doesnt work locally

# thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

from flask import Flask, send_from_directory
import serverless_wsgi
# import boto3

from Map import fullscreen_map

######################## LOGGING ########################
# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-lib
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


######################## APP ########################
app = Flask(__name__)

######################## HOMEPAGE ########################
@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()


######################## LAMBDA WRAPPER ########################
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


######################## FOR LOCAL DEBUGGING ########################

if __name__ == "__main__":
    app.run(debug=True)
