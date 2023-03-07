#! /usr/bin/python3

#
# Downloads JSON from an ArcGIS REST Service to file
#
# URLs must be the query URL.
#
# Example ArcGIS REST Services:
# Zip Codes
# https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/ZIP_Codes/MapServer/0/query
# Parcels (HUGE)
# https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/TCAD_public/MapServer/0/query
#

# Based on code from:
# https://support.esri.com/en/technical-article/000019645
#

import urllib.parse, urllib.request, os, json
import shutil

def download_json_from_arcgis(query_url, destination_filename):
    query_url += "?"
    
    params = {'where': '1=1',
	      'geometryType': 'esriGeometryEnvelope',
	      'spatialRel': 'esriSpatialRelIntersects',
	      'relationParam': '',
	      'outFields': '*',
	      'returnGeometry': 'true',
	      'geometryPrecision':'',
	      'outSR': '',
	      'returnIdsOnly': 'false',
	      'returnCountOnly': 'false',
	      'orderByFields': '',
	      'groupByFieldsForStatistics': '',
	      'returnZ': 'false',
	      'returnM': 'false',
	      'returnDistinctValues': 'false',
	      'f': 'pjson',
# No password 'token': token
    }
    encode_params = urllib.parse.urlencode(params).encode("utf-8")
    
    response = urllib.request.urlopen(query_url, encode_params)
    json = response.read()

    with open(destination_filename, "wb") as ms_json:
        ms_json.write(json)


def download_json_zip_if_needed(query_url, directory_without_slash, destination_json_filename):
    json_full_filename = directory_without_slash + "/" + destination_json_filename
    zip_full_filename = json_full_filename + ".zip"
    if not os.path.isfile(zip_full_filename):
        if not os.path.isfile(json_full_filename):
            download_json_from_arcgis(query_url, json_full_filename)
        # shutil.make_archive("downloads/foo.txt", "zip", "downloads", "foo.txt")
        shutil.make_archive(json_full_filename, 'zip', directory_without_slash, destination_json_filename)

        
# main() is only defined to help test this library

def main():
    print("Running test.")

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
