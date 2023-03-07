#! /usr/bin/python3

#
# This is the program to run to generate all the outputs
#

import download_json_from_arcgis
import os.path
import urllib.request

#
# URLs of downloaded files
#

parcels_query_url = "https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/TCAD_public/MapServer/0/query"

zoning_query_url = "https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/PLANNINGCADASTRE_zoning_small_map_scale/FeatureServer/0/query"

#zoning_ordinance_download_url = "https://data.austintexas.gov/api/geospatial/xt8n-xrjg?accessType=DOWNLOAD&method=export&format=GeoJSON"

appraisal_roll_download_url = "https://traviscad.org/wp-content/largefiles/2022%20Certified%20Appraisal%20Export%20Supp%200_07252022.zip"


def download_file_if_needed(url, filename):
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(url, filename)


#
# The program!
# Downloads files (if necessary), processes them, and generates output files
#
        
def main():

    zipcodes_query_url = "https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/ZIP_Codes/MapServer/0/query"
    directory = "../downloads"
    destination_json_filename = "travis_county_zips.json"
    print("Downloading Travis County Zip Code data")
    print("Source is " + zipcodes_query_url)
    print("Directory is " + directory)
    print("Destination JSON filename is " + destination_json_filename)
    #download_json_from_arcgis(zipcodes_query_url, directory + "/" + destination_json_filename)
    download_json_zip_if_needed(zipcodes_query_url, directory, destination_json_filename)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()


