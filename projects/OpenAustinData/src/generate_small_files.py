#! /usr/bin/env python3

#
# This program shrinks the output from 374,000 parcels to 5,000
#

import sys
import os.path
import shutil

import csv
import pandas as pd
import geopandas as gpd


center_latitude  =  30.268027
center_longitude = -97.742855
count = 5000


def distance_to_center(row):
    lat_diff  = row["LatitudeDecimalDegrees"]  - center_latitude
    long_diff = row["LongitudeDecimalDegrees"] - center_longitude
    return lat_diff**2 + long_diff**2


def main():

    #
    # Check requirements
    #

    needed_dirs = ["downloads/", "inputs/", "tmp/", "outputs/"]
    for dir in needed_dirs:
        if not os.path.exists(dir):
            print("No " + dir + " directory.  Did you run this program in the wrong directory.")
            sys.exit(1)

    #
    #
    #
    
    pza_filename = "outputs/parcels_with_zoning_and_appraisals.csv"    
    polygon_filename = "outputs/polygons.geojson.zip"    

    pza_small_filename = "outputs/pza_small.csv"
    
    if not os.path.isfile(pza_small_filename):
        if not os.path.isfile(pza_filename):
            print("Unable to generate small pza file.  Large file does not exist.")
            sys.exit(1)

        merged_pza = pd.read_csv(pza_filename)
        
        merged_pza["dist_to_center"] = merged_pza.apply( lambda row: distance_to_center(row), axis=1)
        
        #cut_off_value = merged_pza.nsmallest(count, "dist_to_center").max()
        #cut_off_value = merged_pza["dist_to_center"].argsort()[::-1][count]
        cut_off_value = merged_pza.nsmallest(count, "dist_to_center")["dist_to_center"].max()

        print("cutoff = " + str(cut_off_value))
        
        small = merged_pza[merged_pza["dist_to_center"] <= cut_off_value]

        small.to_csv(pza_small_filename)

        
    polygon_small_filename = "outputs/polygons_small.geojson.zip"
    
    if not os.path.isfile(polygon_small_filename):
        if not os.path.isfile(polygon_filename):
            print("Unable to generate small polygon file.  Large file does not exist.")
            sys.exit(1)

        polygons = gpd.read_file(polygon_filename)

        
        small_pza = pd.read_csv(pza_small_filename)
        
        small_polygons = polygons.loc[ polygons["PROP_ID"].isin(small_pza["PROP_ID"]) ]

        print("Writing out small files with polygons")
        small_polygons.to_file("outputs/polygons_small.geojson", driver='GeoJSON')
        shutil.make_archive("outputs/polygons_small.geojson", "zip", "outputs", "polygons_small.geojson")
                                       
    
if __name__ == "__main__":
    # execute only if run as a script
    main()


    
