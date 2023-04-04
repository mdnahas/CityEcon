#! /usr/bin/env python3

#
# Helper functions for downloading files.
# For the ArcGIS REST API, it uses the library "esridumper".
#

import sys
import json
import shutil
import os.path
import json
import requests
import logging

# I didn't take the time to figure out Python's module system.
# This works, but only from the top-level directory.
# Which is GOOD, because the files are placed relative
# to that location.  But it could be improved.

sys.path.append("./src/pyesridump/esridump")
from dumper import EsriDumper


def download_file_if_needed(url, filename):
    if not os.path.isfile(filename):
        if url == "":
            print("Unable to download " + filename + ".  URL not available.")
            return
        # This simple line got 403 as a response.
        #urllib.request.urlretrieve(url, filename)
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)


# This function calls the esridumper library.
# It downloads a "Feature" and writes it as a JSON file
def call_esridumper_library(url, json_full_name):
    # Create logger so we see if something is not working
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)   # logging.INFO
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Call the "dumper", which downloads the data into memory
    dumper = EsriDumper(url,
            parent_logger=logger)

    # Write out all the polygons in GeoJSON format
    with open(json_full_name, "w") as outfile:
        outfile.write('{"type":"FeatureCollection","features":[\n')
        feature_iter = iter(dumper)
        try:
            feature = next(feature_iter)
            while True:
                outfile.write(json.dumps(feature))
                feature = next(feature_iter)
                outfile.write(',\n')
        except StopIteration:
            outfile.write('\n')
        outfile.write(']}')


# This function downloads a feature to a JSON file and ZIPs the file.        
def download_json_zip_if_needed(url, zip_full_filename):
    json_full_filename = zip_full_filename[0:-4]
    slash_location = json_full_filename.find("/")
    directory_without_slash = json_full_filename[:slash_location]
    json_filename = json_full_filename[slash_location+1:]
    if not os.path.isfile(zip_full_filename):
        if not os.path.isfile(json_full_filename):
            print("Downloading from " + url)
            call_esridumper_library(url, json_full_filename)
        # shutil.make_archive("downloads/foo.txt", "zip", "downloads", "foo.txt")
            print("Done download")
        shutil.make_archive(json_full_filename, 'zip', directory_without_slash, json_filename)
