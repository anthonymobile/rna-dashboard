#TODO build out custom html popups solution
# based on last example here https://stackoverflow.com/questions/38171687/adding-a-popup-to-a-geojson-layer-in-folium

import requests
from jinja2 import Environment, FileSystemLoader

#BUG this is creating a memory explosion
#TODO option 1 - increase memory to max
#TODO option 2 - write them out back to disk? same file or separate file?
#TODO option 3 - use a function approach instead of OOP

class LayerBundle():

    def __init__(self, bucket_url, layer_name):
        self.layer_name = layer_name
        self.bucket_url = bucket_url
        self.geojson = self.get_geojson(layer_name)
        self.environment = Environment(loader=FileSystemLoader("templates/"))
        self.render_popups()
        self.render_tooltips()

    def get_geojson(self, layer_name):
        response = requests.get(f"{self.bucket_url}/maps/{layer_name}.geojson")
        return response.json()
    
    def render_popups(self):
        template = self.environment.get_template("popup.html")
        for feature in self.geojson["features"]:
            feature["properties"]["popup"] = template.render(
                properties=feature
                )

        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD", "BLOCK","LOT"], aliases=["Number", "Street", "Block", "Lot"]
        # ),

    def render_tooltips(self):
        template = self.environment.get_template("tooltip.html")
        for feature in self.geojson["features"]:
            feature["properties"]["tooltip"] = template.render(
                test_message="This is a tooltip. It should be pretty sparse" #BUG this
                )

        # tooltip=folium.features.GeoJsonTooltip(
        #     fields=["HNUM", "HADD", "BLOCK","LOT"], 
        #     aliases=["Number", "Street", "Block", "Lot"]
        # ),