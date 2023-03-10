# rna-dashboard

## TODO features to add

### resources
- send clicked lat lon back to python 
    - https://gis.stackexchange.com/questions/313382/click-event-on-maps-with-folium-and-information-retrieval

### punchlist
- Add draw 200 foot radius (from centroid? Check code) on clickd
- customize tooltip formatting
        - Append a computed tooltip column with customised text https://towardsdatascience.com/using-folium-to-generate-choropleth-map-with-customised-tooltips-12e4cec42af2
        - injecting HTML into a folium popup (see last comment) https://gis.stackexchange.com/questions/185897/how-can-i-include-html-in-a-folium-marker-popup
- cloropleth map
    - https://towardsdatascience.com/using-folium-to-generate-choropleth-map-with-customised-tooltips-12e4cec42af2
- Add draw 200 foot radius (from centroid? Check code) on click
    - https://stackoverflow.com/questions/74520790/python-folium-circle-not-working-along-with-popup
    - folium.Circle(
        [lat, long],
        radius=200).add_to(map) #tk? how to scale the circle?

- JC API query on street address (in pupup with linked to records)
    - API https://data.jerseycitynj.gov/api/v2/catalog/datasets/zoning-board-application-74-bowers-st-z22-040-2022/records?where=search%28%2274%20bowers%22%29&limit=10&offset=0&timezone=UTC
- NJ parcels query
- export vacants db to geojson and add layer
— add 3d viewer, buildings layer in a 3d viewer
- clickable SDL portal query (need to get API access via city planning)
- local read/write postgis for adding our own content to map via geoalchemy2.

## TESTING AND DEBUGGING

### www lambda

1. `cd rna_dashboard/functions/www`
2. Start the flask server `python app-local.py`
3. head to http://127.0.0.1:5000/ in your browser to see the map displayed
