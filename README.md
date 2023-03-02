# rna-dashboard

## TODO

### v 0.2
- add a title https://stackoverflow.com/questions/75493570/how-can-i-add-a-text-box-to-folium-with-more-or-less-the-same-behavior-as-the-l
- move map data to S3
- add zoning oerlay
- add street centerlines

### v 0.3
- build out UI / docs
- user testing

### v 0.4
- clickable parcel level query on JC open data (e.g. popup shows data from JC open data, NJparcels, zoning info, etc)


### FUTURE
- clickable SDL portal query (need to get API access via city planning)
- local read/write postgis for adding our own content to map via geoalchemy2.
- click on property to draw 200 foot radius

    folium.Circle(
        [lat, long],
        radius=200).add_to(map) #tk? how to scale the circle?

## TESTING AND DEBUGGING

### www lambda

1. `cd rna_dashboard/functions/www`
2. Start the flask server `python app.py`
3. head to http://127.0.0.1:5000/ in your browser to see the map displayed
# rna-dashboard
# rna-dashboard
