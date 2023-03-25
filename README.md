# rna-dashboard

This is a folium dashboard for a community in Jersey City, NJ. It is a static website.

## features to add

### VIP
- run seeclickfix query and display
    - https://seeclickfix.com/api/v2/issues?lat=40.750650&lng=-74.042520&zoom=18
- layers
    - create RNA building footprints only and add back
- build / stack
    - automate the freeze process
- layout
    change out float for a bottom full-width bar with simple big title
- popups: more query shortcuts
    - NJparcels.com
    - SDL portal (need to get API access via city planning)
- building footprints datum
    - check building footprints for datum shift and fix https://www.directionsmag.com/article/4048
- add a spinning icon while map loads
    - folium's plugin wrapper: https://python-visualization.github.io/folium/plugins.html
        - maybe class folium.plugins.BeautifyIcon?
    - extend folium by writing my own plugin wrapper for https://github.com/makinacorpus/Leaflet.Spin/ ?



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

## credits
thank you https://realpython.com/python-folium-web-maps-from-data/ for the styling and layout tutorial


## to deploy

1. cd to app dir
    
    `cd rna_dashboard/app`

2. build the static site

    `python freeze.py`

3. cd back up and deploy

    `cd ../.. && cdk deploy`

## cleanup a failed deploy

1. `aws cloudformation delete-stack --stack-name rna-dashboard-stack`
2. empty bucket `aws s3 rm s3://rna-dashboard-stack --recursive`
3. `aws s3api delete-bucket --bucket rna-dashboard-stack`