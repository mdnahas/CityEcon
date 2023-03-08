#! /usr/bin/env python3

#
# This is the program to run to generate all the outputs
#

import sys
import os.path
#import zipfile
import subprocess

from download import download_file_if_needed
from download import download_json_zip_if_needed
from convert_fixedwidth_to_CSV import convert_fixedwidth_to_CSV

#
# URLs of downloaded files
#

parcels_url = "https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/TCAD_public/MapServer/0"

zoning_url = "https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/PLANNINGCADASTRE_zoning_small_map_scale/FeatureServer/0"

#zoning_ordinance_download_url = "https://data.austintexas.gov/api/geospatial/xt8n-xrjg?accessType=DOWNLOAD&method=export&format=GeoJSON"

appraisal_roll_download_url = "https://traviscad.org/wp-content/largefiles/2022%20Certified%20Appraisal%20Export%20Supp%200_07252022.zip"



        
        
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
            
    print("Downloading appraisal data")
    download_file_if_needed(appraisal_roll_download_url, "downloads/2022 Certified Appraisal Export Supp 0_07252022.zip")
    
    print("Downloading zoning")
    download_json_zip_if_needed(zoning_url, "inputs", "PLANNINGCADASTRE_zoning_small_map_scale.json")

    print("Downloading parcels")
    download_json_zip_if_needed(parcels_url, "downloads", "TCAD_public.json")
    
    #
    # Unzip Appraisal data and convert to CSV
    #

    appraisal_fw_dir = "tmp/appraisal_fixedwith"
    if not os.path.exists(appraisal_fw_dir):
        os.mkdir(appraisal_fw_dir)
        # Zip file's compression method was not supported.
        #with zipfile.ZipFile("downloads/2022 Certified Appraisal Export Supp 0_07252022.zip", 'r') as zip_ref:
        #    zip_ref.extractall(appraisal_fw_dir)
        subprocess.run(["unzip", "downloads/2022 Certified Appraisal Export Supp 0_07252022.zip", "-d", appraisal_fw_dir])

    appraisal_csv_dir = "tmp/appraisal_CSV"
    if not os.path.exists(appraisal_csv_dir):    
        os.mkdir(appraisal_csv_dir)
    appraisal_files = os.listdir(appraisal_fw_dir)
    for filename in appraisal_files:
        if filename[-4:] != ".TXT":
            print("Not converting file " + filename + " to CSV")
        else:
            full_filename_fw  = appraisal_fw_dir  + "/" + filename
            full_filename_csv = appraisal_csv_dir + "/" + filename[0:-4] + ".csv"
            if not os.path.isfile(full_filename_csv):
                print("converting file " + full_filename_fw + " to CSV")
                convert_fixedwidth_to_CSV(filename, full_filename_fw, full_filename_csv)
                

    
if __name__ == "__main__":
    # execute only if run as a script
    main()


