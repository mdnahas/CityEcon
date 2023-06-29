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

parcels_url = "https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/TCAD_public/MapServer/0"

zoning_url = "https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/PLANNINGCADASTRE_zoning_small_map_scale/FeatureServer/0"

#zoning_ordinance_download_url = "https://data.austintexas.gov/api/geospatial/xt8n-xrjg?accessType=DOWNLOAD&method=export&format=GeoJSON"

appraisal_roll_download_url = "https://traviscad.org/wp-content/largefiles/2022%20Certified%20Appraisal%20Export%20Supp%200_07252022.zip"

#TODO: Zipcode?

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
                
    #
    # Join parcels with zoning file and appraisal file
    #

    print("reading parcels")
    parcels = gpd.read_file("downloads/TCAD_public.json.zip")
    ignore_fields_list = ignore_fields("Parcels")
    parcels = parcels[[column for column in parcels.columns if column not in ignore_fields_list]] 

    
    print("reading zoning")
    zoning = gpd.read_file("inputs/PLANNINGCADASTRE_zoning_small_map_scale.json.zip")
    ignore_fields_list = ignore_fields("Zoning")
    zoning = zoning[[column for column in zoning.columns if column not in ignore_fields_list]] 


    print("computing centroids of parcels")
    # save geometry in a column
    parcels['polygons'] = parcels.geometry

    # set geometry to centroids
    parcels['centroid'] = parcels.geometry.centroid   
    parcels = parcels.set_geometry('centroid')

    # join
    print("joining parcels with zoning")
    parcels_with_zoning = gpd.sjoin(parcels, zoning, how="left", predicate="intersects")

    # free memory
    del parcels 
    del zoning
    gc.collect()
    
    # restore geometry and remove added columns
    parcels_with_zoning = parcels_with_zoning.set_geometry('polygons')
    parcels_with_zoning = parcels_with_zoning[[column for column in parcels_with_zoning.columns if column not in ('centroid','polygons')]]     

    print("reading appraisals")
    appraisals = gpd.read_file("tmp/appraisal_CSV/PROP.csv", ignore_fields=ignore_fields("PROP.TXT"))

    # Make sure prop_id is an int.  I had trouble with this.
    appraisals["prop_id"] = appraisals["prop_id"].astype(int)
    
    print("joining parcels&zoning with appraisals")    
    parcels_with_zoning_and_appraisals = pd.merge(parcels_with_zoning, appraisals, how="left", left_on="PROP_ID", right_on="prop_id")

    print("outputing")

    #remove OBJECTID_left,
    #keep PROP_ID,
    #keep   situs_address,tcad_acres,hyperlink,LatitudeDecimalDegrees,LongitudeDecimalDegrees,
    #remove geometry_x,index_right,OBJECTID_right,
    #keep ZONING_ZTYPE,ZONING_BASE,
    #remove field_1,prop_id,
    #remove prop_type_cd,
    #remove situs_street_prefx,situs_street,situs_street_suffix,situs_city,
    #keep? situs_zip,
    #keep legal_acreage,
    #remove land_hstd_val,land_non_hstd_val,
    #keep? appraised_val,
    #remove ten_percent_cap,assessed_val,hs_exempt,ov65_exempt,ov65s_exempt,dp_exempt,
    #keep imprv_state_cd,land_state_cd,land_acres,
    #remove ownership_pct,market_value,situs_num,situs_unit,geometry_y

    fields_to_remove = [
        "OBJECTID_left",
        "geometry_x","index_right","OBJECTID_right",
        "field_1","prop_id",
        "prop_type_cd",
        "situs_street_prefx","situs_street","situs_street_suffix","situs_city",
        "land_hstd_val","land_non_hstd_val",
        "ten_percent_cap","assessed_val","hs_exempt","ov65_exempt","ov65s_exempt","dp_exempt",
        "ownership_pct","market_value","situs_num","situs_unit","geometry_y"
        ]
    parcels_with_zoning_and_appraisals = parcels_with_zoning_and_appraisals[[column for column in parcels_with_zoning_and_appraisals.columns if column not in fields_to_remove]]
    
    fields_to_rename = {
        #"PROP_ID",
        "situs_address":"address",
        "tcad_acres":"acres_parcel",
        "hyperlink":"hyperlink_to_TCAD",
        "LatitudeDecimalDegrees":"latitude",
        "LongitudeDecimalDegrees":"longitude",
        "ZONING_ZTYPE":"zoning_exact",
        "ZONING_BASE": "zoning_base",
        "situs_zip":"ZIPcode",
        "legal_acreage":"acres_legal",
        "appraised_val":"appraised_value",
        "imprv_state_cd":"improvements_state_code",
        "land_state_cd":"land_state_code",
        "land_acres": "acres_appraisal"
        }
    
    parcels_with_zoning_and_appraisals = parcels_with_zoning_and_appraisals.rename(fields_to_rename, axis=1, errors="raise") 

    old_cols = parcels_with_zoning_and_appraisals.columns.tolist()
    new_cols = ["PROP_ID", "ZONING_ZTYPE", "ZONING_BASE", "tcad_acres", "situs_zip", "situs_address", "imprv_state_cd", "land_state_cd", "LatitudeDecimalDegrees", "LongitudeDecimalDegrees", "legal_acreage", "land_acres", "appraised_val", "hyperlink"]
    for col in old_cols:
        if col not in new_cols:
            new_cols.append(col)
    
    pd.DataFrame(parcels_with_zoning_and_appraisals).to_csv("outputs/lot_data_for_Tim.csv", columns=new_cols)

    
if __name__ == "__main__":
    # execute only if run as a script
    main()


