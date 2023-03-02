# Start the flask server by running:
# python flask_example.py
# head to http://127.0.0.1:5000/ in your browser to see the map displayed
# thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

from flask import Flask, render_template_string
import serverless_wsgi

import geopandas as gpd
import folium

app = Flask(__name__)


# @app.route("/")
# def fullscreen():
#     m = folium.Map(
#         location=(40.746759, -74.042197),
#         zoom_start=16,
#         tiles="cartodb positron"
#         )
#     return m.get_root().render()


@app.route("/")
def fullscreen_parcels():

    m = folium.Map(
        location=(40.746759, -74.042197), zoom_start=16, tiles="cartodb positron"
    )

    parcels_gdf = gpd.read_file(
        "maps/parcels/RNA_Parcel_Basemap_From_2019_JC_OpenData.shp"
    )
    folium.GeoJson(
        # data=parcels_gdf["geometry",'HNUM','HADD'],
        data=parcels_gdf,
        popup=folium.GeoJsonPopup(
            fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        ),
    ).add_to(m)

    return m.get_root().render()


# @app.route("/iframe")
# def iframe():
#     """Embed a map as an iframe on a page."""

#     m = folium.Map()

#     # set the iframe width and height
#     m.get_root().width = "800px"
#     m.get_root().height = "600px"
#     iframe = m.get_root()._repr_html_()

#     return render_template_string(
#         """
#             <!DOCTYPE html>
#             <html>
#                 <head></head>
#                 <body>
#                     <h1>Using an iframe</h1>
#                     {{ iframe|safe }}
#                 </body>
#             </html>
#         """,
#         iframe=iframe,
#     )


# @app.route("/components")
# def components():
#     """Extract map components and put those on a page."""
#     m = folium.Map(
#         width=800,
#         height=600,
#     )

#     m.get_root().render()
#     header = m.get_root().header.render()
#     body_html = m.get_root().html.render()
#     script = m.get_root().script.render()

#     return render_template_string(
#         """
#             <!DOCTYPE html>
#             <html>
#                 <head>
#                     {{ header|safe }}
#                 </head>
#                 <body>
#                     <h1>Using components</h1>
#                     {{ body_html|safe }}
#                     <script>
#                         {{ script|safe }}
#                     </script>
#                 </body>
#             </html>
#         """,
#         header=header,
#         body_html=body_html,
#         script=script,
#     )


#### WRAPPER ###############################################################################
# lambda handler (maps requests via serverless-wsgi)
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


#### DEBUG ###############################################################################
# We only need this for local execution.

if __name__ == "__main__":
    app.run(debug=True)
