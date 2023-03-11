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

    ############################################################
    # MAPS GEOJSON LAYERS
    # layers stack in order they are added (last=top)
    ############################################################

    # Heights Building Footprints
    folium.GeoJson(
        "geojson/heights-building-footprints.geojson",
        #f"{request.base_url}/geojson/heights-building-footprints.geojson",
        name="Building Footprints",
        style_function=lambda feature: {
            'fillColor': 'grey',
            'color': 'black',
            'weight': 0.5,
            'dashArray': '3, 3'
        },
        # tooltip='<b>Heights Bulding Footprints Tooltip</b><br><br>What should go here?',
        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
        # ),
    ).add_to(m)


    # Heights Parcels
    folium.GeoJson(
        "geojson/heights-parcels.geojson",
        # f"{request.base_url}/geojson/heights-parcels.geojson",
        name="Parcels",
        style_function=lambda feature: {
            'fillColor': 'gray',
            'fillOpacity': 0.1,
            'color': 'gray',
            'weight': 0.5,
            'opacity': 0.5,
            # 'dashArray': '5, 5'
        },
        #FIXME is there a way to combine these two approaches — e.g. inject fields but also specify the HTML?
        # see last comment for popup html injection
        # https://gis.stackexchange.com/questions/185897/how-can-i-include-html-in-a-folium-marker-popup

        # # simple HTML tooltip
        # tooltip='<b>Heights Parcel Tooltip</b><br><br>What should go here?',

        # fields in HTML tooltip
        tooltip=folium.features.GeoJsonTooltip(
            fields=["HNUM", "HADD", "BLOCK","LOT"], 
            aliases=["Number", "Street", "Block", "Lot"]
        ),

        # popup=folium.GeoJsonPopup(
        #     fields=["HNUM", "HADD", "BLOCK","LOT"], aliases=["Number", "Street", "Block", "Lot"]
        # ),
    ).add_to(m)

    # # TODO add cloropleth? dwelling units /acre??
    # choropleth = folium.Choropleth(
    #     geo_data = hk_geo,
    #     name = 'choropleth',
    #     data = voter_proportion,
    #     columns = ['Eng_name', 'Proportion'],
    #     key_on = 'feature.properties.name_1',
    #     fill_color = 'YlGn',
    #     fill_opacity = 0.7,
    #     line_opacity = 0.2,
    #     legend_name = '2019年選民登記比例', # Voter Proportion (%) in 2019
    #     highlight = True
    # ).add_to(m)


    #FIXME: How to combine with the parcel pop-up or stop from overriding
    # ############################################################
    # POPUP: Street View access like on-click feature
    # https://www.mkrgeo-blog.com/open-street-view-with-python-folium-map/
    # ############################################################
 
    class LatLngPopup(MacroElement):
        _template = Template(u"""
        {% macro script(this, kwargs) %}
        var {{this.get_name()}} = L.popup();
        function latLngPop(e) {
        data = e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4);
        {{this.get_name()}}
        .setLatLng(e.latlng)
        .setContent( "<H1>LatLngPopup</H1><a href=https://www.google.com/maps?layer=c&cbll=" + data + " target=blank >Google Streetview</a>")
        .openOn({{this._parent.get_name()}})
        }
        {{this._parent.get_name()}}.on('click', latLngPop);

        {% endmacro %}
        """) # noqa

        def __init__(self):
            super(LatLngPopup, self).__init__()
            self._name = 'LatLngPopup'

    latlon = LatLngPopup()

    m.add_child(latlon)


    # RNA Boundaries
    folium.GeoJson(
        "geojson/boundaries-rna.geojson",
        #f"{request.base_url}/geojson/boundaries-rna.geojson",
        name="Parcels",
        style_function=lambda feature: {
            'fillColor': 'none',
            'color': 'green',
            'weight': 4,
            'opacity': 0.5,
            'dashArray': '2, 2'
        },
    ).add_to(m)

    # # Zones
    # folium.GeoJson(
    #     f"{request.base_url}/geojson/jc-zoning-map.geojson", #FIXME PATH
    #     show=False,
    #     name="Zoning",
    #     tooltip='<b>Citywide Zoning Tooltip</b><br><br>What should go here?',
    #     # popup=folium.GeoJsonPopup(
    #     #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
    #     # ),
    # ).add_to(m)


    ############################################################
    # FLOATING TEXTBOX
    ############################################################
    # Injecting custom css through branca macro elements
    # via https://stackoverflow.com/questions/75493570/how-can-i-add-a-text-box-to-folium-with-more-or-less-the-same-behavior-as-the-l
    textbox_css = open("textbox.html").read()
    my_custom_style = MacroElement()
    my_custom_style._template = Template(textbox_css)
    m.get_root().add_child(my_custom_style)

    ############################################################
    # LAYER CONTROL
    ############################################################
    folium.LayerControl().add_to(m)

    ############################################################
    # RETURN MAP
    ############################################################
    return m