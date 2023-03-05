# rna-dashboard

## TESTING AND DEBUGGING

### www lambda

1. `cd rna_dashboard/functions/www`
2. Start the flask server `python app-local.py`
3. head to http://127.0.0.1:5000/ in your browser to see the map displayed


## TODO

### v 0.2

- move to chilltownlabs domain
    - can just create an A record on gandi to point to the API?
        - update the CDK stack to reflect
    - or the reverse? migrate chilltown to route53 and point it back at gandi?


### v 0.3
- build out UI / docs
- user testing

### v 0.4
- clickable parcel level query on JC open data (e.g. popup shows data from JC open data, NJparcels, zoning info, etc)
https://gis.stackexchange.com/questions/313382/click-event-on-maps-with-folium-and-information-retrieval


### FUTURE
— add 3d viewer, buildings layer in a 3d viewer
- clickable SDL portal query (need to get API access via city planning)
- local read/write postgis for adding our own content to map via geoalchemy2.
- click on property to draw 200 foot radius

    folium.Circle(
        [lat, long],
        radius=200).add_to(map) #tk? how to scale the circle?

