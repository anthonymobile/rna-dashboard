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
    logging.info("map url:"+f"{request.base_url}/static/maps/parcels/parcels-2019-heights.geojson")

    # LAYER: Heights Parcels
    folium.GeoJson(
        f"{request.base_url}/static/maps/parcels/parcels-2019-heights.geojson",
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


    # # LAYER: RNA Parcels
    # folium.GeoJson(
    #     f"{request.base_url}/static/maps/parcels/parcels-2019-rna.geojson",
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


    # LAYER: Heights Building Footprints
    folium.GeoJson(
        f"{request.base_url}/static/maps/building-footprints/building-footprints-heights.geojson",
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


    # LAYER: RNA Boundaries
    folium.GeoJson(
        f"{request.base_url}/static/maps/boundaries-rna.geojson",
        name="Parcels",
        style_function=lambda feature: {
            'fillColor': 'none',
            'color': 'green',
            'weight': 4,
            'opacity': 0.5,
            'dashArray': '2, 2'
        },
    ).add_to(m)

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
 

    # # display zoning map
    # folium.GeoJson(
    #     f"{request.base_url}/static/maps/zone-districts-unknown-jersey-city.geojson", #FIXME PATH
    #     name="Zoning",
    #     # popup=folium.GeoJsonPopup(
    #     #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
    #     # ),
    # ).add_to(m)

    # # display census map
    # folium.GeoJson(
    #     f"{request.base_url}/static/maps/tracts-blocks-2018-jersey-city.geojson", #FIXME PATH
    #     name="Census Tracts and Block Groups",
    #     # popup=folium.GeoJsonPopup(
    #     #     fields=["HNUM", "HADD"], aliases=["Number", "Street"]
    #     # ),
    # ).add_to(m)


    #FIXME the styling is terrible, and add my content (maybe load from a markdown file?)
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
    m.get_root().add_child(my_custom_style)


    folium.LayerControl().add_to(m)

    return m