#TODO build out custom html popups solution
# based on last example here https://stackoverflow.com/questions/38171687/adding-a-popup-to-a-geojson-layer-in-folium


import json
import requests

class LayerBundle():

    def __init__(self, bucket_url, layer_name):
        self.layer_name = layer_name
        self.bucket_url = bucket_url
        self.geojson = self.get_geojson(layer_name)
        self.render_popups()
        self.render_tooltips()
        # self.layer_and_popups = self.add_popups(layer_name)

    def get_geojson(self, layer_name):
        response = requests.get(f"{self.bucket_url}/maps/{layer_name}.geojson")
        return response.json()
    
    def render_popups(self):
        #TODO compute the HTML for each popup and add as a property called 'popup' to each feature in self.geojson
        for feature in self.geojson["features"]:
            feature["properties"]["popup"] = "<h2>This is a computed popup.</h2>"
        pass

    def render_tooltips(self):
        for feature in self.geojson["features"]:
            feature["properties"]["tooltip"] = "<h2>This is a computed tooltip.</h2>"
        pass
    


    
'''
# https://stackoverflow.com/questions/38171687/adding-a-popup-to-a-geojson-layer-in-folium

# suburbs_json = json.load(open(file_path, "r"))
# file_path=os.path.join(settings.BASE_DIR,"static/map/state_map.csv")
# suburbs_data = pd.read_csv(file_path)
# suburbs_id_map={}
# for feature in suburbs_json["features"]:
#     feature["id"] = feature["properties"]["STATE_CODE"]
#     suburbs_id_map[feature["properties"]["STATE_NAME"]] = feature["id"]
# suburbs_data["id"] = suburbs_data['state'].apply(lambda x: suburbs_id_map[x])
# suburbs_data.fillna(0)

# def datass(feature):
#     k1=suburbs_data.loc[(suburbs_data['id'] == feature)].values.tolist()
#     print(k1)
#     try:
#         k=int(k1[0][5])
#         # if k <=1:
#         #     risk='No Risk'
#         #     color='#808080'
#         if k<=1:
#             l=k1[0][0]
#             return l
#         if k == 2:
#             risk='Significant Risk'
#             color='#edcf64'
#         elif k == 3:
#             risk='High Risk'
#             color= '#be2a3e'    
        
#         #print(feature,html)
#         return html
#     except:
#         return k1.Suburb_Name


# for feature in suburbs_json["features"]:
#     feature["properties"]["popups"]=datass(feature['id'])
# def style_function_opcity_suburb(feature):
#     k1=suburbs_data[(suburbs_data['id'] == feature['id'])]
#     try:
#         k=int(k1.risk)
#     except:
#         k=0
#     if k >1:
#         return 1
#     else:
#         return 0
# def style_function_suburb(feature):
#     k1=suburbs_data[(suburbs_data['id'] == feature['id'])]
#     try:
#         k=int(k1.risk)
#     except:
#         k=0
#     if k == 1:
#         return '#ffffff'
#     elif k == 2:
#         return '#edcf64'
#     elif k == 3:
#         return '#be2a3e'    
#     else:
#         return '#ffffff'

# m = folium.Map(location=[-23.85077947836127, 134.5773586588719],zoom_start=4)
# folium.GeoJson(
#     suburbs_json,
#     style_function=lambda feature: {
#         'fillColor': style_function_suburb(feature),
#         'color':'black', 
#         'fillOpacity':style_function_opcity_suburb(feature), 
#         'weight': 0.1,
#     },
#     highlight_function=lambda feature: {
#         'fillColor': style_function_suburb(feature),
#         'color':'black', 
#         'fillOpacity': style_function_opcity_suburb(feature), 
#         'weight': 2,
#     },
#     tooltip=folium.features.GeoJsonTooltip(
#         fields=['popups'],
#         labels=False,
#         style=("background-color: white; color: #333333; font-family: arial; 
#         font-size: 12px; padding: 10px;") 
#     )
# ).add_to(m)
# folium.TileLayer('cartodbpositron').add_to(m)
# m=m._repr_html_() #updated
# return render(request, 'test_map.html', {'my_map':m})



#TODO move this to an external file
html=f"""<div class="card col " style="border-radius:6px;border-top: 6px solid {color};"><div class="card-body">
                        <div style='display:flex;justify-content:space-between'">
                            <h6 class="card-title mb-4" style="font-size: 14px;">State:{k1[0][0]}</h6>
                            <h6 class="card-title mb-1" style="font-size: 14px;color: {color}">{risk}<br></h6>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table align-middle table-nowrap mb-0">
                            <thead>
                                <tr>
                                    <th scope="col" >MECHANISM</th>
                                    <th scope="col">%</th>
                                    <th scope="col">INCIDENTS</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>

                                    <td>{k1[0][6]}</td>
                                    <td>{k1[0][8]}</td>
                                    <td >{k1[0][10]}</td>

                                </tr>
                                <tr>

                                    <td >{k1[0][7]}</td>
                                    <td >{k1[0][9]}</td>
                                    <td >{k1[0][11]}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="mb-0" style="font-size: 11px;">
                            FORECAST ACCURACY +-10%
                    </p>
                    <p class="mb-0" style="font-size: 9px;">
                            updated on {k1[0][12]}
                    </p>
                </div>
            </div>          
            """


'''