#! /usr/bin/python3

#
# This is the program to run to generate all the outputs
#

import os.path

from download import download_file_if_needed
from download import download_json_zip_if_needed

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
    if not os.path.exists("downloads/"):
        print("No downloads/ directory.  You ran this in the wrong directory.")
        sys.exit(1)

    if not os.path.exists("inputs/"):
        print("No downloads/ directory.  You ran this in the wrong directory.")
        sys.exit(1)

    
    print("Downloading appraisal data")
    download_file_if_needed(appraisal_roll_download_url, "downloads/2022 Certified Appraisal Export Supp 0_07252022.zip")
    
    print("Downloading zoning")
    download_json_zip_if_needed(zoning_url, "inputs", "PLANNINGCADASTRE_zoning_small_map_scale.json")

    print("Downloading parcels")
    download_json_zip_if_needed(parcels_url, "downloads", "TCAD_public.json")
    
if __name__ == "__main__":
    # execute only if run as a script
    main()


