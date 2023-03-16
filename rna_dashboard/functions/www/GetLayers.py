#TODO build out custom html popups solution
# based on last example here https://stackoverflow.com/questions/38171687/adding-a-popup-to-a-geojson-layer-in-folium

import requests
from jinja2 import Environment, FileSystemLoader

from shapely.geometry import shape
from shapely.geometry.polygon import Polygon

#BUG THIS IS MESS
#BUG need to start over -- read the geojson, 
#BUG leave it as a dict, iterate over it and add the popup and tooltip to each feature, 
#BUG computing things and catching exceptions as needed

class LayerBundle():

    def __init__(self, bucket_url, layer_name):
        self.geojson = self.get_geojson(bucket_url, layer_name)
        self.environment = Environment(loader=FileSystemLoader("templates/"))
        self.template_popup = self.environment.get_template("popup.html")
        self.template_tooltip = self.environment.get_template("tooltip.html")
        self.render_annotations()

    def get_geojson(self, bucket_url, layer_name):
        response = requests.get(f"{bucket_url}/maps/{layer_name}.geojson")
        return response.json()
    
    def render_annotations(self):
        for feature in self.geojson["features"]:
            feature["properties"]["popup"] = self.render_popup(feature)
            feature["properties"]["tooltip"] = self.render_tooltip(feature)
    
    def render_popup(self, feature):
        feature["streetview_url"]=streetview_url=self.render_streetview_url(feature)
        return self.template_popup.render(
            feature=feature
            )

    def render_tooltip(self, feature):
        return self.template_tooltip.render(
            feature=feature
            )
    
    def render_streetview_url(self,feature):
        try:
            polygon: Polygon = shape(feature["geometry"])
            representative_point = polygon.representative_point()
            x = representative_point.x
            y = representative_point.y
            return f"https://www.google.com/maps?layer=c&cbll={x},{y} target=blank"
        except Exception as e:
            print (e)
            return None

    


# TODO variable names need to be wrapped in {{ double curly braces }} in the HTML template
# TODO note that the template gets cached and flask needs to restarted to see changes
# TODO putting dict keys in here doest work when the key is missing  



# class Feature():
#     # after https://joelmccune.com/python-dictionary-as-object/

#     def __init__(self, in_dict:dict):
#         assert isinstance(in_dict, dict)
#         for key, val in in_dict.items():
#             if isinstance(val, (list, tuple)):
#                 setattr(self, key, [Feature(x) if isinstance(x, dict) else x for x in val])
#             else:
#                 setattr(self, key, Feature(val) if isinstance(val, dict) else val)

#         self.popup=self.render_popup()
#         self.tooltip=self.render_tooltip()
            
#     def render_streetview_url(self):
#         try:
#             x = self.properties.centroidx 
#             y = self.properties.centroidy
#             return f"https://www.google.com/maps?layer=c&cbll={x},{y} target=blank"
#         except:
#             return None
        
#     def render_tooltip(self):
#         return template.render(
#             color="red",
#             hnum=(2+2),
#             hadd="Broadway"
#         )
        
#     def render_popup(self):
#         return template.render(
#             color="red",
#             hnum=(2+2),
#             hadd="Broadway",
#             streetview_url=self.render_streetview_url()
#         )
            
