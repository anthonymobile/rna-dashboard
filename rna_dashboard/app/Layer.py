import requests, json
from jinja2 import Environment, FileSystemLoader
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon

class Layer():

    def __init__(self, base_url, layer_name, **kwargs):
        self.kwargs = kwargs
        self.base_url = base_url
        self.layer_name = layer_name
        # self.geojson = self.get_geojson_from_url()
        self.geojson = self.get_geojson_from_disk()
        self.environment = Environment(loader=FileSystemLoader("templates/"))
        self.template_popup = self.environment.get_template("popup.html")
        self.template_tooltip = self.environment.get_template("tooltip.html")
        self.render_annotations()

    def get_geojson_from_url(self):
        response = requests.get(f"{self.base_url}/assets/{self.layer_name}.geojson")
        return response.json()
    
    def get_geojson_from_disk(self):
        with open(f"assets/{self.layer_name}.geojson") as f:
            data = json.load(f)
            return data

    def render_annotations(self):
        for feature in self.geojson["features"]:
            if self.kwargs.get("popups") == True:
                feature["properties"]["popup"] = self.render_popup(feature)
            if self.kwargs.get("tooltips") == True:
                feature["properties"]["tooltip"] = self.render_tooltip(feature)
    
    def render_popup(self, feature):

        return self.template_popup.render(
            hnum=feature["properties"]["HNUM"],
            hadd=feature["properties"]["HADD"],
            block=feature["properties"]["BLOCK"],
            lot=feature["properties"]["LOT"],
            streetview_url=self.render_streetview_url(feature),
            seeclickfix_url=self.render_seeclickfix_url(feature),
            jcportal_url=self.render_jcportal_url(feature),
            )

    def render_tooltip(self, feature):
        return self.template_tooltip.render(
            hnum=feature["properties"]["HNUM"],
            hadd=feature["properties"]["HADD"],
            # feature=feature
            )
    
    def x_y_from_feature(self, feature):
        try:
            polygon: Polygon = shape(feature["geometry"])
            representative_point = polygon.representative_point()
            x = f"{representative_point.x:.6g}"
            y = f"{representative_point.y:.6g}"
            return x, y
        except Exception as e:
            print (e)
            return None, None

    def render_streetview_url(self, feature):
        try:
            x, y = self.x_y_from_feature(feature)
            return f"https://www.google.com/maps?layer=c&cbll={y},{x}"
        except Exception as e:
            print (e)
            return None
    

    def render_seeclickfix_url(self, feature):
        try:
            x, y = self.x_y_from_feature(feature)
            return f"https://seeclickfix.com/api/v2/issues?lat={y}&lng={x}&zoom=18"
        except Exception as e:
            print (e)
            return None

    #FIXME fetch the data, format and insert it with links to the SCF content
    #FIXME this will have to run / render on the server side, how to embed in JS to run on poup?
    def render_seeclickfix_data(self, feature):

        headers = {'Accept': 'application/json'}
        r = requests.get('https://reqbin.com/echo/get/json', headers=headers)
        data = r.json()
        table = []
        for issue in data["issues"]:
            table.append('<li><a href="issue[url]">{issue["title"]}')
        return table

        
    def render_jcportal_url(self, feature):
        try:
            hnum = feature["properties"]["HNUM"]
            hadd = feature["properties"]["HADD"]
            return f"https://data.jerseycitynj.gov/explore/?q={hnum}+{hadd}"
        except Exception as e:
            print (e)
            return "DINGO"
