# rna-dashboard
thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial

## DEBUGGING STATUS AS OF 2023-03-11

1. need to migrate to an ECS/Fargate deplo

## features to add

### VIP
- layout
    change out float for a bottom full-width bar with simple big title
- popups: more query shortcuts
    - NJparcels.com
    - SDL portal (need to get API access via city planning)
- building footprints datum
    - check building footprints for datum shift and fix https://www.directionsmag.com/article/4048

### low priority
- cloropleth map
    - https://towardsdatascience.com/using-folium-to-generate-choropleth-map-with-customised-tooltips-12e4cec42af2
- Add draw 200 foot radius (from centroid? Check code) on click
    - https://stackoverflow.com/questions/74520790/python-folium-circle-not-working-along-with-popup
    - folium.Circle(
        [lat, long],
        radius=200).add_to(map) #tk? how to scale the circle?
- export vacants db to geojson and add layer
— add 3d viewer, buildings layer in a 3d viewer
