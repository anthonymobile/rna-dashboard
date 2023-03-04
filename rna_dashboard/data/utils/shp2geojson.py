'''python shp2geojson.py input.shp output.geojson
'''
# chatgpt wrote this
import argparse
import geopandas as gpd

# Create the argument parser
parser = argparse.ArgumentParser(description='Convert a shapefile to GeoJSON format.')

# Add the input and output file arguments
parser.add_argument('input_file', help='path to the input shapefile')
parser.add_argument('output_file', help='path to the output GeoJSON file')

# Parse the arguments
args = parser.parse_args()

# Load the shapefile into a GeoDataFrame
gdf = gpd.read_file(args.input_file)

# Convert the GeoDataFrame to GeoJSON format
geojson = gdf.to_json()

# Write the GeoJSON to a file
with open(args.output_file, 'w') as f:
    f.write(geojson)
