# this production version is deployed to AWS Lambda via the Serverless Framework
# it loads the static content from S3
# it doesnt work locally

# thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

from flask import Flask, render_template_string, Response, request
import serverless_wsgi

# import geopandas as gpd
import folium
import boto3

app = Flask(__name__)

# Initialize the S3 client
s3 = boto3.client('s3')


def fullscreen_map():
    
    map = folium.Map(
        location=(40.746759, -74.042197), 
        zoom_start=16, 
        tiles="cartodb positron"
    )

    #display RNA parcel basemap
    folium.GeoJson(
        f"{request.base_url}/static/maps/parcels-2019-rna.geojson",
        popup=folium.GeoJsonPopup(
            fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        ),
    ).add_to(map)

    return map


# Define a route to serve the static content
@app.route('/static/<path:path>')
def serve_static_content(path):
    #FIXME: pass bucket name in from paramstore?
    response = s3.get_object(Bucket="rna-dashboard", Key=path) 
    return Response(response['Body'].read(), mimetype=response['ContentType'])

@app.route("/")
def homepage():
    return fullscreen_map().get_root().render()


#### WRAPPER ###############################################################################
# lambda handler (maps requests via serverless-wsgi)
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


#### DEBUG ###############################################################################
# We only need this for local execution.

if __name__ == "__main__":
    app.run(debug=True)
