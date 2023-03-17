import requests
from jinja2 import Environment, FileSystemLoader

from shapely.geometry import shape
from shapely.geometry.polygon import Polygon

class LayerBundle():

    def __init__(self, bucket_url, layer_name, **kwargs):
        self.kwargs = kwargs
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
            if self.kwargs.get("popups") == True:
                feature["properties"]["popup"] = self.render_popup(feature)
            if self.kwargs.get("tooltips") == True:
                feature["properties"]["tooltip"] = self.render_tooltip(feature)
    
    def render_popup(self, feature):
        feature["streetview_url"]=streetview_url=self.render_streetview_url(feature)
        return self.template_popup.render(
            hnum=feature["properties"]["HNUM"],
            hadd=feature["properties"]["HADD"],
            block=feature["properties"]["BLOCK"],
            lot=feature["properties"]["LOT"],
            streetview_url=feature["streetview_url"],
            # feature=feature
            )

    def render_tooltip(self, feature):
        return self.template_tooltip.render(
            hnum=feature["properties"]["HNUM"],
            hadd=feature["properties"]["HADD"],
            # feature=feature
            )
    
    def render_streetview_url(self,feature):
        try:
            polygon: Polygon = shape(feature["geometry"])
            representative_point = polygon.representative_point()
            x = f"{representative_point.x:.6g}"
            y = f"{representative_point.y:.6g}"
            return f"https://www.google.com/maps?layer=c&cbll={y},{x}"
        except Exception as e:
            print (e)
            return None
