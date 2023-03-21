from branca.element import Template, MacroElement
import folium
from folium.elements import *
from Layer import Layer

def fullscreen_map(base_url):

    m = folium.Map(
        location=(40.746759, -74.042197), zoom_start=16, tiles="stamentoner"
    )

    ############################################################
    # MAPS GEOJSON LAYERS
    # layers stack in order they are added (last=top)
    ############################################################

    # Heights Building Footprints
    folium.GeoJson(
        Layer(
            base_url,
            "heights-building-footprints",
            popups=False,
            tooltips=False
        ).geojson,
        name="Building Footprints",
        style_function=lambda feature: {
            'fillColor': 'grey',
            'color': 'black',
            'weight': 0.5,
            'dashArray': '3, 3'
        }
    ).add_to(m)
    
    # Heights Parcels
    folium.GeoJson(
        Layer(
            base_url,
            "heights-parcels",
            popups=True,
            tooltips=True
        ).geojson,
        name="Parcels",
        style_function=lambda feature: {
            'fillColor': 'gray',
            'fillOpacity': 0.1,
            'color': 'gray',
            'weight': 0.5,
            'opacity': 0.5
        },
        tooltip=folium.GeoJsonTooltip(fields=['tooltip'], labels=False),
        popup=folium.GeoJsonPopup(fields=['popup'], labels=False)
    ).add_to(m)
    
    # #BUG update to use Layer class
    # # RNA Boundaries
    # folium.GeoJson(
    #     base_url,
    #     "boundaries-rna",
    #     name="RNA Boundaries",
    #     style_function=lambda feature: {
    #         'fillColor': 'none',
    #         'color': 'green',
    #         'weight': 10,
    #         'opacity': 0.75,
    #         'dashArray': '2, 2'
    #     },
    # ).add_to(m)


    ############################################################
    # FLOATING TEXTBOX
    ############################################################
    # Injecting custom css through branca macro elements
    # via https://stackoverflow.com/questions/75493570/how-can-i-add-a-text-box-to-folium-with-more-or-less-the-same-behavior-as-the-l
    textbox_css = open("templates/textbox.html").read()
    my_custom_style = MacroElement()
    my_custom_style._template = Template(textbox_css)
    m.get_root().add_child(my_custom_style)

    ############################################################
    # LAYER CONTROL
    ############################################################
    folium.LayerControl().add_to(m)

    ############################################################
    # CSS AND JS fOR STREETVIEW
    ############################################################
    m.get_root().header.add_child(CssLink('./static/style.css'))
    m.get_root().html.add_child(JavascriptLink('./static/index.js'))
    m.get_root().header.add_child(JavascriptLink('https://polyfill.io/v3/polyfill.min.js?features=default'))

    ############################################################
    # RETURN MAP
    ############################################################
    return m