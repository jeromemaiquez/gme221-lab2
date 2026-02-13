# GmE 221 - Laboratory Exercise 2

## Overview
This laboratory performs a parcel-landuse overlay analysis using Python (GeoPandas). Spatial data is retrieved from PostGIS using minimal SQL. Overlay, area computation, percentage calculation, and classification are executed in Python. The final output is exported as a GeoJSON file for visualization in QGIS.

---

## Environment Setup
- Python 3.x
- PostgreSQL with PostGIS
- GeoPandas, SQLAlchemy, psycopg2

---

## How to Run
1. Activate the virtual environment
2. Run `analysis.py` to execute the overlay and classification
3. Load the generated GeoJSON file in QGIS

---

## Outputs
- GeoJSON file: `output/dominant_residential.geojson`
- Visualization in QGIS

---

## Reflection - Part B.6

1. The geometries are represented as different formats/objects inside the PostGIS-enabled database vs. inside GeoPandas. While the two are conceptually similar, a process of conversion was necessary to derive the latter from the former. These different representations (PostGIS vs. GeoPandas) are optimized to different sets of purposes and operations (storage and ST operations vs. pandas- and shapely-based operations).

2. This step is considered I/O because the output does not contain any additional information derived from the datasets. This step consisted merely of a conversion from one representation of the spatial data to another.

3. The "Input/Output" characteristic of computational algorithms means that they require some sort of input (e.g., spatial data), which they perform some transformation or computation to derive some sort of output. In this case, the input is the PostGIS table (with the selected columns), which was converted into an output that was a GeoDataFrame object within GeoPandas. However, in the broader scheme of the whole exercise, this step mostly pertains to Input.

## Reflection - Part D.3

1. The initial CRS of the parcels and landuse datasets were in EPSG:4326, which is a geographic CRS. In a geographic CRS (where the Earth is modeled as a globe), the unit of distance is in degrees/radians, not in meters. In different areas of the globe, the same number of radians may translate to wildly different distances. As such, to measure real distance, the datasets must be reprojected into a projected CRS, which assumes one of many flat planes for the Earth and uses meters for distance.

2. Each projection is distorts the surface of the Earth in some way. Thus, different CRS choices have different assumed shapes onto which the globe is projected (i.e., cone, cylinder, or flat plane), different properties of the Earth's surface they preserve best (i.e., angle, distance, or area), and different parts of the globe they portray most accurately (at the expense of others). As such, choosing the right CRS for a given AOI and scale is important to ensure that the resulting area values are accurate.

3. In one sense, not really. The new shapes are not real-world objects in and of themselves, but simply overlaps of two sets of spatial objects (parcels and landuse). In another sense, these new shapes can be thought to represent relationships between the two aforementioned layers, which can now be analyzed after having been generated.

4. Classification is the step that transforms the new additional information (i.e., parcel/landuse areas and overlap percentages) into a direct answer to a question (i.e., which parcels are dominated by residential landuse?). The ability to answer these spatial questions (across various domains) is what enables spatial analysis to become full-fledged decision support.

5. Yes. Since the analysis focuses on areas of the parcels and landuse areas, any error in the geometries will result in errors in the area values provided. This may be more prominent in smaller parcels, where any minor error may result in a large error in the overlap percentage, thus leading to major changes in their classification.

6. Changing the dominance threshold will either expand or shrink the spatial pattern, but not entirely change it. The most change may be observed in the edges of residential vs. non-residential parcels, or new hotspots may arise in otherwise non-residential dominated areas.

## Reflection - Part F

I chose the 2nd spatial question: _which parcels had no single landuse fragment exceeding 60%?_ I copied the default algorithmic steps to prepare the spatial data from `analysis.py`: CRS transformation, total area calculation, overlay, and overlap area calculation. 

However, to answer the question, I first made use of the .dissolve() method, where I grouped the landuse fragments by parcel, each of which had a list of the landuse area percentages. I then performed thresholding for each of these percentage values per parcel. Using the Python all() function followed by the filtering syntax of pandas, I only retained those parcels where all percentages satisfied the <60% threshold. 

Since the question was a little more complex than the first one (residential-dominant parcels), the algorithmic logic ended up being a little more complex as well. I initially used lambda functions to test the threshold for ALL `"percentage"` values for each parcel. However, I realized that a simpler solution is possible: sort the landuse fragments by `"parcel_pin"` and `"percentage"`, get the first row per parcel via `.dissolve("parcel_pin", aggfunc="first")` (i.e., the largest landuse fragment per parcel), and then test if the largest fragment is under 60%. For each parcel, if the largest fragment is already under the 60% threshold, the rest of the fragments will also be under this threshold, thus satisfying the spatial question.