# QGIS notes

## Vocabulary 

GeoPackage --- a database format for storing GIS and other data

Leaflet --- javascript library for displaying maps on the web.  You need to make "tiles" first.  Leaflet will display the tiles.


## HOWTOS:

### HOWTO: Add layer

In toolbar, click on icon with 3 squares on top of each other with a "plus sign".  (Tooltip says "Data Source Manager".)   

For files with the "gpkg" extension: Select "GeoPackage" on the left side.  Click the "new" button (at the top).  Select the file.  Click the "connect" button (at the top).  Select the layer you want in the table.  Click the "Add" button (at the bottom).   

For files with the "geojson" extension: Select "Vector" on the left side.  At the top, "Source Type" should be "file".  Under "Source", at the extreme right click on "...".  Select the file.  Click the "Add" button (at the bottom).   

<!-- How to create a small dataset to work with? -->

### HOWTO: Add Plugin

From the menu, select "Plugins", and then "Manage and Install Plugins".  It will download a list of available plugins from QGIS's repository.


### HOWTO: Export a subset

Use selection tool (in the middle, looks like a rectangle, a dotted rectangle, and a mouse pointer).

Select the area.

Go to Layers, the layer you want, and right click.  Mouse over "Export" and, from the submenu, select "Save Selected Features as..."


### HOWTO: Intersect zoning with parcels

- compute centroid of each parcel.  The centroid is a point inside the parcel.
- determine which zoning polygon the centroid lies in.


### HOWTO: Find the length of a lot on the street ("curb length")

Mark Isley said you will need to:

- download road lines
- "buffer" the road lines (expand the boundary by a small amount, so that they overlap the lots)
- intersect to identify the buffered line _inside_ each parcel
- length of the _buffered_ line will tell you the curb length.

### HOWTO: Compute time to drive from a parcel to center of city

Mark Isley said you will need to:

- You will need a "routing"
- You will need a "weighted cost surface"

### HOWTO: Compute which parcels are near a particular parcel

- "buffer" the particular parcel
- you can test which parcels intersect the buffered parcel

### HOWTO: Compute how close each parcel is to a major highway

- you can use "proximity search", which computes "distance to the closest X"

### HOWTO: Determine how square or round a parcel is

- you can divide the area of the parcel by the longest internal line segement

### HOWTO: Compute the square footage allowed under zoning laws

- ?

### HOWTO: Compute the height of a building allowed on a parcel under Austin's "Compatibility" law

- select all the single family parcels
- "dissolve" merges multiple polygons into 1 polygon
- "buffer" around the dissolved polygon, for each height limit level (20ft)
- repeat buffering for the 30ft, 40ft, etc. height limits
- intersect buffered polygons with parcels
- merge the intersecting with the parcel to determine compatibility limit
  


