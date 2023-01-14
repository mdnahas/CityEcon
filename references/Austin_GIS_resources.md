# Austin GIS Resources

# Software

-  [QGIS](https://www.qgis.org) is free software to view maps and manipulate GIS data.

# Data

- [Parcel shapefiles for Travis County](https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/TCAD_public/MapServer/0)  This is the outline of each lot.  This is a HUGE file.  It takes hours to download.  You want to save it to your diskdrive and use the saved copy, rather than download it each time.
    - PROP_ID is the key field for identifying parcels
    - Shape__Area is the parcel's area in square feet.

- Basemap (background map) from OpenStreetMap: Install the "QuickMapServices" plugin.  In the toolbar, there will be a little globe with a "plus sign".  (The tooltip will say "QuickMapService".)  Click on that.  In the pop-up menu, select "OSM" and then "OSM Standard".



- Appraisal data from TCAD (Travis County Appraisal District).  You can download appraisal data from the "2022 Appraisal Roll Export" link on [this page](https://traviscad.org/publicinformation).  It contains data like the appraised value, size, state zoning code, number of structures, squarefootage, etc..  The data is fixed-width.  The fields are described in the "Appraisal Export Layout" file.


[Austin's subdivision cases](https://data.austintexas.gov/Building-and-Development/Subdivision-Cases/s7gx-9m54)

- [Roads from USGS](https://carto.nationalmap.gov/arcgis/rest/services/transportation/MapServer)  People use rivers and highways as reference points and you can download the highways here.  The largest highways are "controlled-access highways".  

- [County Boundaries in Texas](https://services.arcgis.com/KTcxiTD9dsQw4r7Z/ArcGIS/rest/services/Texas_County_Boundaries/FeatureServer/0)
