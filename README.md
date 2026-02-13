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

3. The "Input/Output" characteristic of computational algorithms means that they require some sort of input (e.g., spatial data), which they perform some transformation or computation to derive some sort of output. In this case, the input is the PostGIS table (with the selected columns), which was converted into an output that was a GeoDataFrame object within GeoPandas.