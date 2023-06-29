#! /usr/bin/env python3

import os
import sys
import csv


def main():
    year_str = "2023"
    
    #
    # Check requirements
    #

    needed_dirs = ["downloads/", "inputs/", "tmp/", "outputs/"]
    for dir in needed_dirs:
        if not os.path.exists(dir):
            print("No " + dir + " directory.  Did you run this program in the wrong directory.")
            sys.exit(1)


    # Read in taxable value file
    with open("tmp/appraisal_CSV_" + year_str + "/PROP.csv", newline="") as input_file:
        reader = csv.DictReader(input_file)

        with open("outputs/zillow_compare_" + year_str + ".csv", 'w', newline='') as output_file:
            fieldnames = ["prop_id",
                          "ownership_pct",
                          "prop_type_cd",
                          "imprv_state_cd",
                          "land_state_cd",
                          "situs_num",
                          "situs_street_prefx",
                          "situs_street",
                          "situs_street_suffix",
                          "situs_city",
                          "situs_zip",
                          "situs_unit",
                          "legal_acreage",
                          "land_acres",
                          "market_value",
                          "assessed_val"]

            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:

                if row["prop_type_cd"] != "R":
                    #print("Skipping property type " + row["prop_type_cd"])
                    continue

                if row["land_state_cd"] != "A1":
                    #print("Skipping land type " + row["imprv_state_cd"])
                    continue
                    
                if row["imprv_state_cd"] != "A1":
                    #print("Skipping improvement type " + row["imprv_state_cd"])
                    continue
                    
                if float(row["ownership_pct"]) != 100.0:
                    print("Skipping partial owned " + row["ownership_pct"])
                    continue

                output_row = dict()
                for f in fieldnames:
                    output_row[f] = row[f]
                writer.writerow(output_row)


if __name__ == "__main__":
    # execute only if run as a script
    main()
                
