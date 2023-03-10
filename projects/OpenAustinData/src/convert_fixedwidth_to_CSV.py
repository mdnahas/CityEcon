#! /usr/bin/env python3

# Initial version written by Mark Isley.

#
# Converts TCAD's files with fixed-width fields
# into CSV files with headers
#

import pandas as pd
import openpyxl


# Excel file describing columns in fixed-width files
description_excel_file = "inputs/New-Legacy8.0.25_2-Appraisal Export Layout.xlsx"

# The sheet of the Excel file with the data
description_excel_sheet = "TP File Layout"

# The rows in the Excel file that describe each fixed-width file.
# These are RANGES, so the second value is the last row PLUS ONE.
description_excel_rows = {
    "APPR_HDR.TXT": (25, 37),
    "PROP.TXT": (56, 491),
#    "PROP_ENT.TXT": (506, 682),   # 7GB file
    "TOTALS.TXT": (687, 830),
    "ABS_SUBD.TXT": (836, 838),
    "STATE_CD.TXT": (855, 860),
    "IMP_INFO.TXT": (877, 888),
    "IMP_DET.TXT": (901, 913),
    "IMP_ATR.TXT": (928, 935),
    "LAND_DET.TXT": (947, 966),
    "AGENT.TXT": (974, 985),
    "ARB.TXT": (993, 999),
    "LAWSUIT.TXT": (1006, 1011),
    "ENTITY.TXT": (1016, 1018),
    "COUNTRY.TXT": (1025, 1027),
    "MOBILE_HOME_INFO.TXT": (1059, 1071),
    "TAX_DEFERRAL_INFO.TXT": (1095, 1103)
}


def convert_fixedwidth_to_CSV(filename, src_full_filename, dest_full_filename):
    if filename not in description_excel_rows:
        print("Could not find description of fixed-width file named " + filename + ".  Skipping.")
        return

    # tuple assignment!
    (start_row, end_row) = description_excel_rows[filename]

    # extract column descriptions from Excel file
    # I'm not sure why it is "start_row-2".
    # (May be rows start at 0 and it includes the header row?)
    colspec = pd.read_excel(description_excel_file, sheet_name=description_excel_sheet, skiprows=start_row-2, nrows=(end_row-start_row), engine='openpyxl').iloc[:,:6]

    propraw = pd.read_fwf(src_full_filename, widths=colspec.Length, header=0)

    propraw.columns=list(colspec['Field Name'])

    propraw.to_csv(dest_full_filename)


#
# Testing
#

def main():
    filename = "APPR_HDR.TXT"
    (start_row, end_row) = description_excel_rows[filename]

    print("From " + str(start_row) + " to " + str(end_row))
    
    colspec = pd.read_excel(description_excel_file, sheet_name=description_excel_sheet, skiprows=start_row-2, nrows=(end_row-start_row), engine='openpyxl').iloc[:,:6]

    print(str(colspec))
    
    

if __name__ == "__main__":
    # execute only if run as a script
    main()

    