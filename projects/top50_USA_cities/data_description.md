# Top 50 American Cities

[This spreadsheet](city_dataset.csv) has a variety of data from the 50 largest cities by estimated metro population in 2021.  It's great for quickly testing an idea to see if a trend exists.

**Warning: Be aware that the data comes from regions with different bounaries.**

HUD's rents are for "Fair Market Rent" (FMR) areas.  HUD's homeless numbers are for "Continuity of Care" (CoC) areas.  These not consistently aligned with metro areas nor cities.

INRIX's regions are also inconsisent.  (San Jose is part of San Francisco, Riverside part of Los Angeles, and Virginia Beach part of Norfolk.)

**Warning: times are not necessarily aligned in data**

HUD's median rents are **published** in Fiscal Year 2023, but are calculated of earlier data.

## List of fields and sources:

-  Metro area population (US Census 2021 est., 2020, 2010)
-  City population (US Census 2021 est., 2020, 2010)
-  City's area
-  Price of a cheap lot in City (Zillow, 1%ile in Sept. 2021)
-  Price of a cheap apartment in City (1bed+1bath, Zillow 1%ile in Sept. 2021)
-  Median rent (HUD FY2023 and FY2013) 
-  Metro GDP (2018, 2017) 
-  Median lot size and price-per-sqft (<a href="https://www.angi.com/articles/lot-size-index.htm">from Angi.com</a>)
-  Overall homeless and unsheltered homeless (HUD 2019)
-  Last-mile travel speed and hours lost to congestion [INRIX 2021](https://inrix.com/scorecard/)


## Notes taken while collecting data:

Zillow data collection started Sept 17th, 2022.

Lots come from Zillow.com.
I only considered "agent listings".
Lots had to be listed in the last 90 days
Went to round(# available) and then searched for "valid" lot
- had sqft
- had road
- had address (may be #0 on that street)
- was residential (not commercial, not parking lot, no alley)
- nothing left on lot (e.g., old foundation)
- not auction (opening bid at auction)

Apartments/Condos/Co-ops from Zillow.com.
1+ beds, 1+ baths
Listed within 30 days.
Valid listings had:
- had sqft
- has address
! counted many rooms at same address as "1".
! only selected ads with single room at address
3rd ad may have been sponsored.  It was counted as a property except when less than 10.


- Ignored this place in Miami.  I didn't believe it had 1896 sqft. https://www.zillow.com/homedetails/6733-NW-2nd-Ct-3-Miami-FL-33150/2076941032_zpid/
- Seattle is 220 sqft, which is very small.  Especially compared to pictures.   Next would have been this at $1100 and 512 sqft https://www.zillow.com/homedetails/4750-15th-Ave-NE-307-Seattle-WA-98105/2070768044_zpid/
- Ignored this place in Las Vegas.  Didn't believe 5200 sqft. https://www.zillow.com/homedetails/2304-Sunrise-Ave-9-Las-Vegas-NV-89101/2069790629_zpid/
- Ignored indianapolis.  didn't believe 2225 sqft https://www.zillow.com/homedetails/1529-E-Michigan-St-Indianapolis-IN-46201/88918320_zpid/
- Ignored cleveland.  didn't believe 2400 sqft https://www.zillow.com/homedetails/3651-E-55th-St-3-Cleveland-OH-44105/2096510665_zpid/
- Ignored richmond   didn't believe 32 sqft https://www.zillow.com/homedetails/2863-Hull-St-APT-A-Richmond-VA-23224/2061837472_zpid/
- Ignored Louisville   didn't believe 2886 sqft https://www.zillow.com/homedetails/1349-Olive-St-Louisville-KY-40211/73604936_zpid/


10% lot size done on Sept. 21st, 2022.

- In D.C., skipped parking lots.
- In Boston, skipped parking lots.
- In San Francisco ... only 17 lots.  Accepted 2nd lot, but it's questionable.  (On a hillside.)
- San Diego had 14 lots without sizes.  Chose 10%ile of those that did.
- Baltimore the lot was 1 price for 3 lots.  Wasn't sure if size was 1 lot or all.  Took next lot.
- Orlando - accepted undisclosed address because others were disclosed.
- Virginia Beach - skipped 3 0-size lots.  took next
- Providence - skipped lot with no size
- Richmond - skipped 2 lots with no size.  Took 10%ile of the rest.
- New Orleans --  10+40+40+36=126 lots with 0 size.  Took 10%ile of rest


Median lot size came from Angi.com.
It reports Zillow's median lot size in MSA (not city!) from May 2022.
https://www.angi.com/articles/lot-size-index.htm
I was able to extract data from their table
https://embed.neomam.com/the-2022-us-lot-size-index/table/


Median rent comes from this HUD page: https://www.huduser.gov/portal/datasets/50per.html   Not clear what it means.
