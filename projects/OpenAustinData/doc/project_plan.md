# Open Austin Housing Data Project Plan

This project would take a lot of Austin and Travis County's open housing data and put it in a simple format that housing researchers and advocates could use.

## Goal

Austin and Travis County have a lot of data on housing.  But it is in different places and different formats.  This project would collect the data interesting to housing researchers and advocates in a single place and in an easy-to-use format.

For every property in Travis County, we currently have:

- Address 
- Latitude & Longitude
- The shape of each property's boundary ("GIS polygon")
- If inside the City of Austin, its zoning.  E.g., "SF-3".
- The current owner of the property
- Tax data for multiple years, including appraised value and assessed value
- If it is owner-occupied or a rental property
- If it is owner-occupied, the year it qualified for the homestead exemption

We hope to add:

- *near future* City of Austin Zoning in the format most people expect (e.g., "SF-3")
- *near future* What's on the property: building height, squarefootage, mobile homes, etc.
- *near future* Its tax entities, which includes city, school district, ACC, etc.
- *near future* How much tax was paid to each entity
- *near future* If inside the City of Austin, its Council Member district
- *near future* The curb length of the property
- *far future* How long it takes to drive to downtown (6th and Congress Ave.)
- *far future* Links to zoning cases and subdivision cases about this property
- *far future* Links to construction permits, business permits, ...
- *far future* Data on 911 calls at (or near) this property
- *far future* Closest park, library, police station, fire station, etc.
- *far future* When the property was last sold
- *far future* Include data from Williamson and Hays Counties?
- *far future* Anything interesting from [data.austintexas.gov](https://data.austintexas.gov/browse)


## Uses

With this easy-to-use data, City Council Member staff will be able to evaluate changes to the zoning code.  Austin's zoning code is the cause of our high rent.  And our high rent is the cause of our homeless problem.

This data will also be useful to housing researchers.  They can study how different factors, like highway noise and drive time, affects property prices.  They can study how tax policy affects people moving.  (California has a tax policy that discourages moving and has high house prices in many cities.)  They can study how the Austin grew and changed over time.

*Warning* This data is currently open, but inconvenient.  Making it easy to use may have repercussions.  Insiders, like developers and realtors, may use this to help themselves financially.  Politicians may use it to link other data, like donor locations and voting patterns.  


## Technology

This project will use git for source control.

This project will use Markdown or HTML for documentation.

This project will use python3 for code.  The GeoPandas library will be used for manipulating polygons.  

For most data, this project will use CSV files following the [RFC 4180 format](https://datatracker.ietf.org/doc/html/rfc4180.html).  These files may be compressed using Zip.

For the polygons describing the shape of properties, zones, districts, etc., this project will use the ["GeoJSON" format](https://geojson.org/).  These files may be compressed using Zip.  (NOTE: Mark Isley recommended the GeoPackage format, which has the extension ".gpkg".  We might want to revisit this decision at some point in the future.)

The GIS software [QGIS](https://www.qgis.org) will be used to test files. 


## About GIS

GIS stands for "geographic information systems".  It is a collection of software for working with data on land and land boundaries.  It is used by city planners, geologist, mapmakers, archiologist, and others.  They make maps and display data on maps.  Maps with data are called "[choropleth maps](https://en.wikipedia.org/wiki/Choropleth_map)", which is the most awkward word I've ever heard.

GIS data can be thought of as a database, where some of the pieces of data are polygons.  For example, one piece of data in a row might be the polygon that marks the boundary of the property.  Other data in the same row might be the property's owner, descriptions of the buildings on the property, etc..

GIS software is basically a map viewer with a lot of database operations built in.  [QGIS](https://www.qgis.org) is the open-source GIS software that we'll be using.  It can load files that contain data.  It can generate choropleth maps.  It can manipulate the data, such as intersect polygons or do a database join of two files.

GIS files can be huge.  Travis County's parcel file is 187M.  There are web-based protocols for sending parts of files.  GIS software can download just the part that the user is viewing or working on.  It's pretty cool.

Every GIS file has a CRS, which stands for the Coordinate Reference System.  GIS files use 2D polygons to encode boundaries.  But the earth is not flat and, thanks to plate tectonics, things move around.  So, each file with polygons specifies how points on the physical earth are mapped onto a plane.  The mathematical function for doing that is the CRS.

Different GIS files often have different CRS.  The CRS always introduces some distortion.  Each file's creator will choose the CRS that works best with their data.  We have chosen a single CRS for our data.  We translate the polygons from other CRSes to our chosen CRS.  Our chosen CRS is GeoJSON's default CRS, which is known as "EPSG:4326".  In it, points are identified by latitude and longitude and they are mapped on to an elipsoid known as "WGS84".  (It is an elipsoid, not a sphere, because the earth is not perfectly round.)  

Other CRSes we will occasionally encounter are:

- UTM, which has various zones.  Central Texas is in UTM zone 14 North.   UTM is measured in meters.  "EPSG:32614" is WGS84 with UTM zone 14N.   [This map](https://tpwd.texas.gov/publications/pwdpubs/media/pwd_mp_e0100_1070af_24.pdf) has the UTM zones for Texas.

- A state plane CRS.  Texas has 5 state-planes and Austin is in "State Plane Zone 3".  It is measured in feet.  (Is this "EPSG:2277"?  [This page](https://epsg.io/2277) calls it "Texas Central" and it uses "NAD83" elipsoid.")  [This map](https://tpwd.texas.gov/publications/pwdpubs/media/pwd_mp_e0100_1070af_24.pdf) has the Texas state-planes.  

- [Web Mercator](https://en.wikipedia.org/wiki/Web_Mercator_projection).  This is the projection used by most online mapping tools, such as Google Maps.   Coordinates are in the range 0 to 256, with (0,0) in the upper-left near Alaska and (256,256) in the lower-right near Australia.  It is known officially as "EPSG:3857".  (It also appears as "EPSG:3785" and "EPSG:900913".)

## Contributing

At the moment, we're using the directory "projects/OpenAustinData/" in this git repository: [https://github.com/mdnahas/CityEcon/](https://github.com/mdnahas/CityEcon/).

At the moment, we're communicating by an email thread.  To be added to the thread, email [openaustin@mike.nahasmail.com](mailto:openaustin@mike.nahasmail.com).

## More information

There is a list of links to the data we want to merge on [this page](Austin_GIS_resources.html).

There are some notes on how to use QGIS on [this page](QGIS_user_notes.html)

There is are notes on [understanding the data in the files](understanding_files.html).
