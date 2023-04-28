#! /usr/bin/env python3

#
# This is the program to run to generate all the outputs
#

import sys
import os.path
#import zipfile
import shutil
import subprocess
import gc

import csv
import pandas as pd
import geopandas as gpd

from download import download_file_if_needed
from download import download_json_zip_if_needed
from convert_fixedwidth_to_CSV import convert_fixedwidth_to_CSV

#
# URLs of downloaded files
#

# Parcels are 455MB uncompressed, 80MB compressed
parcels_url = "https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/TCAD_public/MapServer/0"
parcels_local_file = "downloads/TCAD_public.json.zip"

# Zoning is 51MB uncompressed, 12MB compressed
zoning_url = "https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/PLANNINGCADASTRE_zoning_small_map_scale/FeatureServer/0"
zoning_local_file = "inputs/PLANNINGCADASTRE_zoning_small_map_scale.json.zip"

# Appraisal are 260MB compressed
appraisals = {
    "2023" : { "url": "https://traviscad.org/wp-content/largefiles/2023%20Appraisal%20Export%20Supp%200_04242023.zip",
               "local_file": "downloads/2023 Appraisal Export Supp 0_04242023.zip" },
    
    "2022" : { "url": "https://traviscad.org/wp-content/largefiles/2022%20Certified%20Appraisal%20Export%20Supp%200_07252022.zip",
               "local_file" : "downloads/2022 Certified Appraisal Export Supp 0_07252022.zip" },

    "2021" : { "url": "https://traviscad.org/wp-content/largefiles/2021-08-02_008042_APPRAISAL_STD%20EXPORT%20R%26P%20ALLJUR%20AS%20OF%202021.zip",
               "local_file" : "downloads/2021-08-02_008042_APPRAISAL_STD EXPORT R&P ALLJUR AS OF 2021.zip" },

    # 2012 appraisal file, from Open Records Request - R004028-112122
    "2012" : { "url" : "",
               "local_file" : "downloads/2019-08-03_007107_APPRAISAL_R_P_ALLJUR_AS_OF_2012.zip"}
}


def ignore_fields(filename):
    result = []
    
    with open('src/which_columns.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row["File"] == filename and row["OutputField"].strip() == "":
                result.append(row["Field"])
            if row["OutputField"].strip() != "" and row["Field"].strip() != row["OutputField"].strip():
                print("Warning: code does not (yet) support renaming output field from " + row["Field"].strip() + " to " + row["OutputField"].strip())

    return result


def pandas_read_csv_ignore_cols(filename, ignore_cols):
    cols = list(pd.read_csv(filename, nrows =1))

    not_ignored_cols = list( set(cols) - set(ignore_cols) )
    
    return pd.read_csv(filename, usecols = not_ignored_cols)


#
# The program!
# Downloads files (if necessary), processes them, and generates output files
#
        
def main():
    #
    # Check requirements
    #

    needed_dirs = ["downloads/", "inputs/", "tmp/", "outputs/"]
    for dir in needed_dirs:
        if not os.path.exists(dir):
            print("No " + dir + " directory.  Did you run this program in the wrong directory.")
            sys.exit(1)

    #if os.listdir("tmp/") != [ ".gitignore" ]:
    #    print("The tmp/ directory is not empty.  Stopping.")
    #    sys.exit(1)
            
    #
    # Download data 
    #
            
    print("Downloading parcels")
    download_json_zip_if_needed(parcels_url, parcels_local_file)

    print("Downloading zoning")
    download_json_zip_if_needed(zoning_url, zoning_local_file)

    for year_str in appraisals:
        print("Downloading appraisal data " + year_str)
        download_file_if_needed(appraisals[year_str]["url"], appraisals[year_str]["local_file"])
    
    
    #
    # Unzip Appraisal data and convert to CSV
    #

    for year_str in appraisals:
        if not os.path.isfile(appraisals[year_str]["local_file"]):
            print("No appraisal file for " + year_str + ".  Skipping.")
            continue
        print("Converting appraisal files for " + year_str + " to CSV.")
        appraisal_fw_dir = "tmp/appraisal_fixedwidth_" + year_str
        if not os.path.exists(appraisal_fw_dir):
            print("  making directory for fixedwidth files for " + year_str)
            os.mkdir(appraisal_fw_dir)
            # Zip file's compression method was not supported.
            #with zipfile.ZipFile("downloads/2022 Certified Appraisal Export Supp 0_07252022.zip", 'r') as zip_ref:
            #    zip_ref.extractall(appraisal_fw_dir)
            print("  unzipping fixed-width files for " + year_str)
            subprocess.run(["unzip", appraisals[year_str]["local_file"], "-d", appraisal_fw_dir])

        appraisal_csv_dir = "tmp/appraisal_CSV_" + year_str
        if not os.path.exists(appraisal_csv_dir):    
            print("  making directory for CSV files for " + year_str)
            os.mkdir(appraisal_csv_dir)
        appraisal_files = os.listdir(appraisal_fw_dir)
        for filename in appraisal_files:
            if filename[-4:] != ".TXT":
                print("  Not converting file " + filename + " to CSV")
            else:
                full_filename_fw  = appraisal_fw_dir  + "/" + filename
                full_filename_csv = appraisal_csv_dir + "/" + filename[0:-4] + ".csv"
                if not os.path.isfile(full_filename_csv):
                    print("  converting file " + full_filename_fw + " to CSV")
                    convert_fixedwidth_to_CSV(filename, full_filename_fw, full_filename_csv)
                
    #
    # Write polygons to their own file
    #
    print("Writing pure polygons file.")
    polygon_filename = "outputs/polygons.geojson.zip"    
    if not os.path.isfile(polygon_filename):
        print("  reading parcels")
        parcels = gpd.read_file(parcels_local_file)

        # just geometry and prop_id
        print("Writing out file with just polygons")
        pure_geo = gpd.GeoDataFrame(parcels[["geometry", "PROP_ID"]])
        pure_geo.to_file("outputs/polygons.geojson", driver='GeoJSON')
        shutil.make_archive("outputs/polygons.geojson", "zip", "outputs", "polygons.geojson")

    # free memory
    gc.collect()
        
    #
    # Join parcels with zoning file 
    #
    print("Merging parcel file with zoning file.")

    pz_filename = "outputs/parcels_with_zoning.csv"    
    if not os.path.isfile(pz_filename):
        print("  reading parcels")
        parcels = gpd.read_file(parcels_local_file)
        ignore_fields_list = ignore_fields("Parcels")
        parcels = parcels[[column for column in parcels.columns if column not in ignore_fields_list]] 

        print("  reading zoning")
        zoning = gpd.read_file(zoning_local_file)
        ignore_fields_list = ignore_fields("Zoning")
        zoning = zoning[[column for column in zoning.columns if column not in ignore_fields_list]] 

        print("  computing centroids of parcels")
        # save geometry in a column
        parcels['polygons'] = parcels.geometry

        # set geometry to centroids
        print("KNOWN WARNING: This program generates a warning regarding \"centroid\".  We should fix it, but I think it is okay for now.")
        parcels['centroid'] = parcels.geometry.centroid   
        parcels = parcels.set_geometry('centroid')

        # join
        print("  joining parcels with zoning")
        parcels_with_zoning = gpd.sjoin(parcels, zoning, how="left", predicate="intersects")

        # Remove created columns
        parcels_with_zoning = parcels_with_zoning[[column for column in parcels_with_zoning.columns if column not in ('OBJECTID_left','OBJECTID_right')]]     

        # restore geometry and remove columns added for sjoin
        parcels_with_zoning = parcels_with_zoning.set_geometry('polygons')
        parcels_with_zoning = parcels_with_zoning[[column for column in parcels_with_zoning.columns if column not in ('centroid','polygons')]]     

        print("Writing parcels&zoning file")
        without_geo = pd.DataFrame(parcels_with_zoning).drop(columns=["geometry"])
        without_geo.to_csv(pz_filename)

    # free memory
    gc.collect()
       

    #
    # Merge in data from appraisal 
    # 
    print("Merging appraisal files with parcels&zoning file.")

    pza_filename = "outputs/parcels_with_zoning_and_appraisals.csv"    
    if not os.path.isfile(pza_filename):
        print("  reading parcels&zoning file")
        merged_pza = pd.read_csv(pz_filename)

        for year_str in appraisals:
            if not os.path.isfile(appraisals[year_str]["local_file"]):
                print("  No appraisal file for " + year_str + ".  Skipping.")
                continue
    
            print("reading appraisals for " + year_str)
            appraisals_prop = pandas_read_csv_ignore_cols("tmp/appraisal_CSV_" + year_str + "/PROP.csv", ignore_fields("PROP.TXT"))
            
            # Make sure prop_id is an int.  I had trouble with this.
            appraisals_prop["prop_id"] = appraisals_prop["prop_id"].astype(int)

            # The code below does a LEFT JOIN.
            # It keeps 1 record per parcel.
            # Some properties have multiple owners and have multiple
            # rows in the appraisal file.  This join just takes one
            # from the appraisal file.  Any one.  The following is
            # just some info to make sure we stay aware of this.

            # I ran the following code for 2022.
            # Only 83 out of 470534 were partial owners.
            # appraisals_prop["ownership_pct"] = appraisals_prop["ownership_pct"].astype(float)
            # num_multiple_owners = (appraisals_prop["ownership_pct"] != 100.0).sum()
            # print("  " + str(num_multiple_owners) + " out of " + str(len(appraisals_prop)) + " appraisal records have multiple owners.  Picking one.")

            # rename fields to add year of appraisal
            rename_dict = dict()
            for col in appraisals_prop.columns:
                if col != "prop_id":
                    rename_dict[col] = year_str + "_" + col
            appraisals_prop = appraisals_prop.rename(rename_dict, axis=1, errors="raise") 

            print("  joining parcels&zoning with appraisals from " + year_str)    
            merged_pza = pd.merge(merged_pza, appraisals_prop, how="left", left_on="PROP_ID", right_on="prop_id")

        print("outputing")
        # Has columns "geometry" and "centroid"
        pd.DataFrame(merged_pza).to_csv(pza_filename)

    
if __name__ == "__main__":
    # execute only if run as a script
    main()


