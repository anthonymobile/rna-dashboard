# this production version is deployed to AWS Lambda via the Serverless Framework
# it loads the static content from S3
# it doesnt work locally

# thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

from flask import Flask, render_template_string, Response, request
import serverless_wsgi
from branca.element import Template, MacroElement

# import geopandas as gpd
import folium
import boto3

app = Flask(__name__)

# Initialize the S3 client
s3 = boto3.client("s3")


def fullscreen_map():

    map = folium.Map(
        location=(40.746759, -74.042197), zoom_start=16, tiles="cartodb positron"
    )
    

    # display JC parcel basemap
    folium.GeoJson(
        f"{request.base_url}/static/maps/parcels-2019-jersey-city.geojson",
        name="Parcels",
        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        # ),
    ).add_to(map)
    

    # # display RNA parcel basemap
    # #FIXME doesnt work, bad geojson export?
    # folium.GeoJson(
    #     f"{request.base_url}/static/maps/rna-parcels-2019.geojson",
    #     name="RNA Parcels",
    #     # popup=folium.GeoJsonPopup(
    #     #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
    #     # ),
    # ).add_to(map)

    # display zoning map
    folium.GeoJson(
        f"{request.base_url}/static/maps/zone-districts-unknown-jersey-city.geojson",
        name="Zoning",
        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        # ),
    ).add_to(map)

    # display census map
    folium.GeoJson(
        f"{request.base_url}/static/maps/tracts-blocks-2018-jersey-city.geojson",
        name="Census Tracts and Block Groups",
        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        # ),
    ).add_to(map)

    # display building footprints
    folium.GeoJson(
        f"{request.base_url}/static/maps/buildings-footprints-2018-jersey-city.geojson",
        name="Building Footprints",
        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        # ),
    ).add_to(map)

    folium.LayerControl().add_to(map)

    #TODO can we move this to a separate file?
    # via https://stackoverflow.com/questions/75493570/how-can-i-add-a-text-box-to-folium-with-more-or-less-the-same-behavior-as-the-l
    # Injecting custom css through branca macro elements and template, give it a name
    textbox_css = """
    {% macro html(this, kwargs) %}
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Textbox Project</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer"/>
        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

        <script>
        $( function() {
            $( "#textbox" ).draggable({
            start: function (event, ui) {
                $(this).css({
                right: "auto",
                top: "auto",
                bottom: "auto"
                });
            }
            });
        });
        </script>
    </head>

    <body>
        <div id="textbox" class="textbox">
        <div class="textbox-title">Textbox (draggable)</div>
        <div class="textbox-content">
            <p>You can put whatever content here.<br>You can create as many elements and positon them all over the map.</p>
            <p>You can delete the script that makes it draggable and all script links that come with it.</p>
            <p>You can add a link to a local CSS file in the head and past the css in it instead of here.</p>
            <p>You can find a way to make it collapsible with JS or CSS, it's a normal HTML div after all.</p>
        </div>
        </div>
    
    </body>
    </html>

    <style type='text/css'>
    .textbox {
        position: absolute;
        z-index:9999;
        border-radius:4px;
        background: rgba( 28, 25, 56, 0.25 );
        box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
        backdrop-filter: blur( 4px );
        -webkit-backdrop-filter: blur( 4px );
        border: 4px solid rgba( 215, 164, 93, 0.2 );
        padding: 10px;
        font-size:14px;
        right: 20px;
        bottom: 20px;
        color: orange;
    }
    .textbox .textbox-title {
        color: darkorange;
        text-align: center;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 22px;
        }
    </style>
    {% endmacro %}
    """
    # configuring the custom style (you can call it whatever you want)
    my_custom_style = MacroElement()
    my_custom_style._template = Template(textbox_css)

    # Adding my_custom_style to the map
    map.get_root().add_child(my_custom_style)



    return map


# Define a route to serve the static content
@app.route("/static/<path:path>")
def serve_static_content(path):
    # FIXME: pass bucket name in from paramstore?
    response = s3.get_object(Bucket="rna-dashboard", Key=path)
    return Response(response["Body"].read(), mimetype=response["ContentType"])


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
