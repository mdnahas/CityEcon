#! /usr/bin/env python3

#
# This is the program to run to generate all the outputs
#

import sys
import os.path
#import zipfile
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
            if row["File"] == filename and row["Ignore"].strip() != "":
                result.append(row["Field"])

    return result
        
        
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
            os.mkdir(appraisal_fw_dir)
            # Zip file's compression method was not supported.
            #with zipfile.ZipFile("downloads/2022 Certified Appraisal Export Supp 0_07252022.zip", 'r') as zip_ref:
            #    zip_ref.extractall(appraisal_fw_dir)
            subprocess.run(["unzip", appraisals[year_str]["local_file"], "-d", appraisal_fw_dir])

        appraisal_csv_dir = "tmp/appraisal_CSV_" + year_str
        if not os.path.exists(appraisal_csv_dir):    
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
    # Join parcels with zoning file and appraisal file
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
        parcels['centroid'] = parcels.geometry.centroid   
        parcels = parcels.set_geometry('centroid')

        # join
        print("  joining parcels with zoning")
        parcels_with_zoning = gpd.sjoin(parcels, zoning, how="left", predicate="intersects")

        # restore geometry and remove added columns
        parcels_with_zoning = parcels_with_zoning.set_geometry('polygons')
        parcels_with_zoning = parcels_with_zoning[[column for column in parcels_with_zoning.columns if column not in ('centroid','polygons')]]     

        pd.DataFrame(parcels_with_zoning).to_csv(pz_filename)

        
    # free memory
    gc.collect()
        

        
    sys.exit(1)

    print("reading appraisals")
    appraisals_old = gpd.read_file("tmp/appraisal_CSV/PROP.csv", ignore_fields=ignore_fields("PROP.TXT"))

    # Make sure prop_id is an int.  I had trouble with this.
    appraisals_old["prop_id"] = appraisals_old["prop_id"].astype(int)

### RIGHT JOIN???
    print("joining parcels&zoning with appraisals")    
    parcels_with_zoning_and_appraisals = pd.merge(parcels_with_zoning, appraisals_old, how="left", left_on="PROP_ID", right_on="prop_id")

    print("outputing")
    # Has columns "geometry" and "centroid"
    pd.DataFrame(parcels_with_zoning_and_appraisals).to_csv("outputs/parcels_with_zoning_and_appraisals.csv")

    
if __name__ == "__main__":
    # execute only if run as a script
    main()


