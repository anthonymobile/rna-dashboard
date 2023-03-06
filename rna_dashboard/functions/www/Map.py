from branca.element import Template, MacroElement
import folium
from flask import request

# ENABLE LOGGING
# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-lib
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def fullscreen_map():

    m = folium.Map(
        location=(40.746759, -74.042197), zoom_start=16, tiles="cartodb positron"
    )
    
    logging.info(f"request.base_url: {request.base_url}")
    logging.info("map url:"+f"{request.base_url}/static/parcels-2019-heights.geojson")


    ############################################################
    # STATIC GEOJSON LAYERS
    ############################################################

    # Heights Parcels
    folium.GeoJson(
        f"{request.base_url}/static/heights-parcels.geojson",
        name="Parcels",
        style_function=lambda feature: {
            'fillColor': 'gray',
            'fillOpacity': 0.1,
            'color': 'gray',
            'weight': 0.5,
            'opacity': 0.5,
            # 'dashArray': '5, 5'
        },
        popup=folium.GeoJsonPopup(
            fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        ),
    ).add_to(m)


    # # RNA Parcels
    # folium.GeoJson(
    #     f"{request.base_url}/static/rna-parcels.geojson",
    #     name="RNA Parcels",
    #     style_function=lambda feature: {
    #         'fillColor': 'green',
    #         'color': 'black',
    #         'weight': 2,
    #         # 'dashArray': '5, 5'
    #     },
    #     popup=folium.GeoJsonPopup(
    #         fields=["HNUM", "HADD"], aliases=["Number", "Street"]
    #     ),
    # ).add_to(m)


    # Heights Building Footprints
    folium.GeoJson(
        f"{request.base_url}/static/heights-building-footprints.geojson",
        name="Building Footprints",
        style_function=lambda feature: {
            'fillColor': 'grey',
            'color': 'black',
            'weight': 0.5,
            'dashArray': '3, 3'
        },
        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        # ),
    ).add_to(m)


    # RNA Boundaries
    folium.GeoJson(
        f"{request.base_url}/static/boundaries-rna.geojson",
        name="Parcels",
        style_function=lambda feature: {
            'fillColor': 'none',
            'color': 'green',
            'weight': 4,
            'opacity': 0.5,
            'dashArray': '2, 2'
        },
    ).add_to(m)

    # Zones
    folium.GeoJson(
        f"{request.base_url}/static/jc-zoning-map.geojson", #FIXME PATH
        name="Zoning",
        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        # ),
    ).add_to(m)



    ############################################################
    # POPUP
    ############################################################

    # Streetview in popup
    #FIXME this works but the 2nd method is probably better for users, and we want to combine with othe data in the popup
    #HOWTO methods are at https://www.mkrgeo-blog.com/open-street-view-with-python-folium-map/
    class ClickForOneMarker(folium.ClickForMarker):

        _template = Template(u"""
        {% macro script(this, kwargs) %}
        var new_mark = L.marker();
        function newMarker(e){
        new_mark.setLatLng(e.latlng).addTo({{this._parent.get_name()}});
        new_mark.dragging.enable();
        new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
        var lat = e.latlng.lat.toFixed(4),
        lng = e.latlng.lng.toFixed(4);
        new_mark.bindPopup("<a href=https://www.google.com/maps?layer=c&cbll=" + lat + "," + lng + " target=blank >Google Street View</a>");
        parent.document.getElementById("latitude").value = lat;
        parent.document.getElementById("longitude").value =lng;
        };
        {{this._parent.get_name()}}.on('click', newMarker);
        {% endmacro %}
        """) # noqa

    def __init__(self, popup=None):
        super(ClickForOneMarker, self).__init__(popup)
        self._name = 'ClickForOneMarker'


    click_for_marker = ClickForOneMarker()

    m.add_child(click_for_marker)
 

    ############################################################
    # FLOATING TEXTBOX
    ############################################################

    # Injecting custom css through branca macro elements
    # via https://stackoverflow.com/questions/75493570/how-can-i-add-a-text-box-to-folium-with-more-or-less-the-same-behavior-as-the-l
    textbox_css = open("textbox.html").read()

    # configuring the custom style (you can call it whatever you want)
    my_custom_style = MacroElement()
    my_custom_style._template = Template(textbox_css)

    # Adding my_custom_style to the map
    m.get_root().add_child(my_custom_style)

    ############################################################
    # LAYER CONTROL
    ############################################################

    folium.LayerControl().add_to(m)

    ############################################################
    ############################################################

    return m