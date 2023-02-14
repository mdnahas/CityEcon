# QGIS notes

# Add layer

In toolbar, click on icon with 3 squares on top of each other with a "plus sign".  (Tooltip says "Data Source Manager".)   

For files with the "gpkg" extension: Select "GeoPackage" on the left side.  Click the "new" button (at the top).  Select the file.  Click the "connect" button (at the top).  Select the layer you want in the table.  Click the "Add" button (at the bottom).   

For files with the "geojson" extension: Select "Vector" on the left side.  At the top, "Source Type" should be "file".  Under "Source", at the extreme right click on "...".  Select the file.  Click the "Add" button (at the bottom).   

<!-- How to create a small dataset to work with? -->

## Plugins 

From the menu, select "Plugins", and then "Manage and Install Plugins".  It will download a list of available plugins from QGIS's repository.




## GeoPackage --- a database format for storing GIS and other data


## Leaflet --- javascript library for displaying maps on the web.  You need to make "tiles" first.  Leaflet will display the tiles.


# GeoPandas --- Python library for manipulating GIS files



# Export a subset

Use selection tool (in the middle, looks like a rectangle, a dotted rectangle, and a mouse pointer).

Select the area.

Go to Layers, the layer you want, and right click.  Mouse over "Export" and, from the submenu, select "Save Selected Features as..."



## Intersect zoning with platts



# Install Anaconda to manage python environments

https://www.anaconda.com/

# Installing geopandas (with conda)

https://geopandas.org/en/stable/getting_started/install.html

* checkout "spatial joins" and "centroid"


? How to find the length of curb on the lot?
  --- need road lines
  --- "buffer" them (expand the boundary by a small amount, so that they overlap the lots)
  --- Intersect to identify the buffered line _inside_ each parcel
  --- The length of the _buffered_ line will tell you the curb length.


? How to do drive time?
   --- "routing"
   --- "weighted cost surface"

? Are your neighbors rich?
   --- "buffer" each parcel
   --- intersect the other parcels

? How close are you to a major highway?
   --- "proximity search" = distance to the closest X (but much harder than other techniques)

? How square/round is a parcel?
   --- area / longest internal line segment?

? How to compute the McMansion bounding box (buildable sqft)?
  ---

? Compatibility
  --- select all the single family parcels
  --- "dissolve" merges multiple polygons into 1 polygon
  --- "buffer" around the dissolved polygon, for each height limit level (20ft)
  ! can repeattedly buffer for the 30ft, 40ft, etc. limit
  --- intersect with parcels
  --- merge the intersecting with the parcel to determine compatibility limit
  

