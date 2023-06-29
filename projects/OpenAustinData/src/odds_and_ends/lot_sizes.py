#! /usr/bin/env python3

import sys
import csv


def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def main():
    if len(sys.argv) != 3:
        print("Needs 2 arguments.  input filename, output filename")

    # sys.argv[0] is name of the program.
    with open(sys.argv[1], newline="") as input_file:
        reader = csv.DictReader(input_file)
        
        with open(sys.argv[2], 'w', newline='') as output_file:

            fieldnames = reader.fieldnames
            fieldnames.append("Classification")

            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                output_row = row
                
                if row["ZONING_ZTYPE"] == "":
                    output_row["Classification"] = "NotAustin"
                elif "SF-3" not in row["ZONING_ZTYPE"]:
                    output_row["Classification"] = "NotSF3"
                elif not is_float(row["2022_land_acres"]):
                    output_row["Classification"] = "NoSize"
                else:
                    sqft = 43560 * float(row["2022_land_acres"]) / 10000.0
                    if sqft < 5750:
                        output_row["Classification"] = "NoADU"
                    elif sqft < 7000:
                        output_row["Classification"] = "ADU"
                    elif sqft < 11500:
                        output_row["Classification"] = "Duplex"
                    else:
                        output_row["Classification"] = "Splittable"

                writer.writerow(output_row)

        
if __name__ == "__main__":
    # execute only if run as a script
    main()
                
