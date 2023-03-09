# Open Austin Housing Data Project Plan

This project would take a lot of Austin and Travis County's open housing data and put it in a simple format that housing researchers and advocates could use.

## Goal

Austin and Travis County have a lot of data on housing.  But it is in different places and different formats.  This project would collect the data interesting to housing researchers and advocates in a single place and in an easy-to-use format.

For every property in Travis County, we want:

- The shape of each property's boundary
- What's on the property: squarefootage and height of buildings, etc.
- The owner of the property
- When the property was last sold
- Tax data, especially the appraised value and assessed value
- If we can, does the owner live there?  (Does it get the "homestead exemption"?)
- If inside the City of Austin, its zoning.  E.g., "SF-3".
- If inside the City of Austin, its Council Member district
- *optional* Its tax districts, which includes school district, ACC, etc.
- *optional* The curb length of the property
- *optional* How long it takes to drive to downtown (6th and Congress Ave.)
- *optional* Create files with the same data but for different years.
- *future* Links to zoning cases and subdivision cases about this property
- *future* Links to construction permits, business permits, ...
- *future* Data on 911 calls at (or near) this property
- *future* Closest park, library, police station, fire station, etc.
- *future* Anything interesting from [data.austintexas.gov](https://data.austintexas.gov/browse)

## Uses

With this easy-to-use data, City Council Member staff will be able to evaluate changes to the zoning code.  Austin's zoning code is the cause of our high rent.  And our high rent is the cause of our homeless problem.

This data will also be useful to housing researchers.  They can study how different factors, like highway noise and drive time, affects property prices.  They can study how tax policy affects people moving.  (California has a tax policy that discourages moving and has high house prices in many cities.)  They can study how the Austin grew and changed over time.

*Warning* This data is currently open, but inconvenient.  Making it easy to use may have repercussions.  Insiders, like developers and realtors, may use this to help themselves financially.  Politicians may use it to link other data, like donor locations and voting patterns.  

## Technology

This project will use git for source control.

This project will use Markdown or HTML for documentation.

This project will use python3 for code.  The GeoPandas library will be used for manipulating polygons.  

For most data, this project will use CSV files following the [RFC 4180 format](https://datatracker.ietf.org/doc/html/rfc4180.html).  They may be compressed.  

For the polygons describing the shape of properties, zones, districts, etc., Mark Isley recommends the GeoPackage format, which has the extension ".gpkg".  There is also a ["GeoJSON" format](https://geojson.org/), which we should consider.

The GIS software [QGIS](https://www.qgis.org) will be used to test files. 

## About GIS

GIS stands for "geographic information systems".  It is a mix of software and data for working with land boundaries and data about land.  It is used city planners, geologist, mapmakers, archiologist, and others.  They make maps and display data on maps.  Maps with data are called "[choropleth maps](https://en.wikipedia.org/wiki/Choropleth_map)", which is the most awkward word I've ever heard.

GIS data can be thought of as a database, where some of the pieces of data are polygons.  The data for properties will include a polygon that marks the boundary of the property and other data, such as the property's owner, buildings on the property, etc..

GIS software is basically a map viewer with a lot of database operations built in.  [QGIS](https://www.qgis.org) is the open-source GIS software that we'll be using.  It can load files that contain data.  It can generate choropleth maps.  It can manipulate the data, such as intersect polygons or do a database join of two files.

GIS files can be huge.  Travis County's parcel file is 187M.  There are web-based protocols for sending parts of files.  GIS software can download just the part that the user is viewing or working on.  It's pretty cool.

Every GIS file has a CRS, which stands for the Coordinate Reference System.  The GIS files use 2D polygons to encode boundaries.  But the earth is not flat and, thanks to plate tectonics, things move around.  So, each file with polygons specifies how points on the physical earth are mapped onto a plane.  The mathematical function for doing that is the CRS.

Different GIS files often have different CRS.  The CRS always introduces some distortion.  Each file's creator will choose the CRS that works best with their data.  We will need to pick a single CRS for our data and translate the polygons from other CRSes to our chosen CRS.  The likely choice of CRS is GeoJSON's default CRS, where points are identified by latitude and longitude and mapped on to an elipsoid known as "WGS84".  (It is an elipsoid, not a sphere, because the earth is not perfectly round.)  

## Contributing

At the moment, we're using the directory "projects/OpenAustinData/" in this git repository: [https://github.com/mdnahas/CityEcon/](https://github.com/mdnahas/CityEcon/).

At the moment, we're communicating by an email thread.  To be added to the thread, email [openaustin@mike.nahasmail.com](mailto:openaustin@mike.nahasmail.com).

## More information

There is a list of links to the data we want to merge on [this page](Austin_GIS_resources.html).

There are some notes on how to use QGIS on [this page](QGIS_user_notes.html)


