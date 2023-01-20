# Austin GIS Resources

# Software

-  [QGIS](https://www.qgis.org) is free software to view maps and manipulate GIS data.

# Basic Data

- [Parcel shapefiles for Travis County](https://gis.traviscountytx.gov/server1/rest/services/Boundaries_and_Jurisdictions/TCAD_public/MapServer/0)  This is the outline of each lot.  This is a HUGE file.  It takes hours to download.  You want to save it to your diskdrive and use the saved copy, rather than download it each time.
    - PROP_ID is the key field for identifying parcels
    - Shape__Area is the parcel's area in square feet.

<!-- I have it saved locally to:  file:///home/mike/Desktop/Home/projects/AURA/min_lot_size_calculation/TCAD_Parcels.gpkg -->

- Basemap (background map) from OpenStreetMap: Install the "QuickMapServices" plugin.  In the toolbar, there will be a little globe with a "plus sign".  (The tooltip will say "QuickMapService".)  Click on that.  In the pop-up menu, select "OSM" and then "OSM Standard".

- [Austin City Zoning Zones](https://data.austintexas.gov/Locations-and-Maps/Zoning-Ordinance/xt8n-xrjg)  You will to click the "Export" button and select "GEOJSON".  

- Appraisal data from TCAD (Travis County Appraisal District).  You can download appraisal data from the "2022 Appraisal Roll Export" link on [this page](https://traviscad.org/publicinformation).  It contains data like the appraised value, size, state zoning code, number of structures, squarefootage, etc..  The data is fixed-width.  The fields are described in the "Appraisal Export Layout" file.


# Other Data

- [City of Austin GIS Website](https://www.austintexas.gov/department/gis-data)  No data.  Just links to stuff.  

- [Austin's Open Data on Locations sorted by populariy](https://data.austintexas.gov/browse?category=Locations+and+Maps&sortBy=most_accessed&utf8=%E2%9C%93)   Open data include zoning cases, construction permits, business permits, police stations, pools, City-owned trees, etc..  Some specific ones are below.

- [Address to Austin Zoning](https://data.austintexas.gov/Locations-and-Maps/Zoning-by-Address/nbzi-qabm)
    - BASE_ZONE field has stuff like "SF-3"


- [Austin's City Council Districts](https://maps.austintexas.gov/GIS/CouncilDistrictMap/)


- [Austin's subdivision cases](https://data.austintexas.gov/Building-and-Development/Subdivision-Cases/s7gx-9m54)

<!-- Need roads from TCAD, to find curb width -->

- [Roads from USGS](https://carto.nationalmap.gov/arcgis/rest/services/transportation/MapServer)  People use rivers and highways as reference points and you can download the highways here.  The largest highways are "controlled-access highways".  

- [Boundaries of Travis and Surrounding Counties](https://data.austintexas.gov/Locations-and-Maps/Counties/u6wx-p5c8) There is also a map of [All of Texas County Boundaries](https://services.arcgis.com/KTcxiTD9dsQw4r7Z/ArcGIS/rest/services/Texas_County_Boundaries/FeatureServer/0)

- [Travis County Lakes and Rivers](https://data.austintexas.gov/Locations-and-Maps/Lakes-and-Rivers/p2uq-mkbt)