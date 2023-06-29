#! /usr/bin/env python3

import os
import sys
import csv


def main():
    data_year_str = "2023"
    taxrate_year_str = "2022"
    
    #
    # Check requirements
    #

    needed_dirs = ["downloads/", "inputs/", "tmp/", "outputs/"]
    for dir in needed_dirs:
        if not os.path.exists(dir):
            print("No " + dir + " directory.  Did you run this program in the wrong directory.")
            sys.exit(1)

    # Read in tax rates
    # sys.argv[0] is name of the program.
    tax_rates = dict()
    with open("inputs/TaxRates.csv", newline="") as input_file:
        reader = csv.DictReader(input_file)

        for row in reader:
            tax_rates[row["entity_id"]] = row


    # Read in taxable value file
    with open("tmp/appraisal_CSV_" + data_year_str + "/PROP_ENT.csv", newline="") as input_file:
        reader = csv.DictReader(input_file)

        with open("outputs/taxes_austin_" + data_year_str + ".csv", 'w', newline='') as output_file:
            fieldnames = ["prop_id", "owner_id", "market_value", "tax", "hs_savings", "cap_savings", "coa_hs_savings"]

            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            output_row = dict()
            output_valid = True
            seen_Austin = False
            
            for row in reader:
                # if on a new property, output row and restart
                if "prop_id" in output_row and row["prop_id"] != output_row["prop_id"]:
                    if output_valid and seen_Austin:
                        writer.writerow(output_row)
                    #elif not output_valid:
                    #    print("output invalid")
                    #else:
                    #    print("not seen Austin")
                    output_row = dict()

                if "prop_id" not in output_row:
                    output_row["prop_id"] = row["prop_id"]
                    output_row["owner_id"] = row["owner_id"]
                    output_row["market_value"] = row["market_value"]
                    output_row["tax"] = 0.0
                    output_row["hs_savings"] = 0.0
                    output_row["cap_savings"] = 0.0
                    output_row["coa_hs_savings"] = 0.0
                    output_valid = True
                    seen_Austin = False

                if row["owner_id"] != output_row["owner_id"]:
                    # Property has multiple owners.
                    # This is rare, so just skip it.
                    output_valid = False
                    continue
                    
                if row["entity_id"] not in tax_rates:
                    print("Could not find tax rates for entity " + row["entity_id"] + " for prop " + row["prop_id"])
                    sys.exit(1)

                tr = tax_rates[row["entity_id"]]

                # if we don't have a tax rate, ignore this row.
                if tr[taxrate_year_str + " tax rate"].strip() == "":
                    if row["entity_id"].strip() == "1000":
                        # TCAD has its own entity. Not sure why.
                        # State doesn't have a tax rate for it.
                        # Just skip this entity and still valid.
                        pass
                    else:
                        #print("No tax rate for " + row["entity_name"])
                        output_valid = False
                    continue

                if row["taxable_val"].strip() != "":
                    output_row["tax"] += float(row["taxable_val"]) * 0.01 * float(tr[taxrate_year_str + " tax rate"])
                if row["hs_amt"].strip() != "":
                    output_row["hs_savings"] += float(row["hs_amt"]) * 0.01 * float(tr[taxrate_year_str + " tax rate"])
                if row["hs_cap"].strip() != "":
                    output_row["cap_savings"] += float(row["hs_cap"]) * 0.01 * float(tr[taxrate_year_str + " tax rate"])
                # Note:
                # Additional exemptions are in rows like "ov65_amt"
                # All exemptions are in "ab_amt"
                
                if row["hs_amt"].strip() != "" and row["entity_id"].strip() == "1002":
                    output_row["coa_hs_savings"] += float(row["hs_amt"]) * 0.01 * float(tr[taxrate_year_str + " tax rate"])

                if row["entity_id"].strip() == "1002":
                    seen_Austin = True
                

if __name__ == "__main__":
    # execute only if run as a script
    main()
                
