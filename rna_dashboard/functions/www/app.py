# this production version is deployed to AWS Lambda via the Serverless Framework
# it loads the static content from S3
# it doesnt work locally

# thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-lib
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from flask import Flask, render_template_string, Response, request, send_file
import serverless_wsgi
import boto3

from Map import fullscreen_map

# ENABLE LOGGING
# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-lib
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

# route: homepage
@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()

# route: map layers

# # this chatbot code works for html files, but it think its being bypassed and the static files are being served directly
# # e.g. https://rna.crowdr.org/static/test.html works but none of the geojson does because the content type is wrong?
# # Define a route to serve the static content
# @app.route("/static/<path:path>")
# def serve_static_content(path):
#     s3 = boto3.resrouce("s3")
#     logging.info(f"Fetching {path} from s3")
#     response = s3.get_object(Bucket="rna-dashboard", Key=path) 
#     return Response(response["Body"].read(), mimetype=response["ContentType"])

#FIXME this error is a file not found error
# json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

#TODO test this Chat GPT code
@app.route('/static/<path:path>')
def serve_geojson(path):
    s3 = boto3.resource('s3')
    bucket_name = 'rna-dashboard' # TODO pass bucket name in, this causes huge problems
    key = path
    obj = s3.Object(bucket_name, key)
    return send_file(obj.get()['Body'], mimetype='application/json')

# #TODO2 try Flask-S3 
# # https://flask-s3.readthedocs.io/en/latest/
# from flask_s3 import FlaskS3
# s3 = FlaskS3()
#
# def start_app():
#     app = Flask(__name__)
#     s3.init_app(app)
#     return app




#### WRAPPER ###############################################################################
# lambda handler (maps requests via serverless-wsgi)
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


#### DEBUG ###############################################################################
# We only need this for local execution.
if __name__ == "__main__":
    app.run(debug=True)
