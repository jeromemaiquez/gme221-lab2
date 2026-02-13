import geopandas as gpd
from sqlalchemy import create_engine

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221"
user = "postgres"
password = "postgres"

# Create connection string
conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

# Create SQLAlchemy engine
engine = create_engine(conn_str)

# Minimal SQL queries (no spatial operations)
sql_parcel = "SELECT parcel_pin, geom FROM public.parcel"
sql_landuse = "SELECT name, geom FROM public.landuse"

# Load data into GeoDataFrames
parcels = gpd.read_postgis(sql_parcel, engine, geom_col="geom")
landuse = gpd.read_postgis(sql_landuse, engine, geom_col="geom")

# print(parcels.head())
# print(landuse.head())

# Reproject to EPSG:3395 for area calculations
parcels = parcels.to_crs(epsg=3395)
landuse = landuse.to_crs(epsg=3395)

parcels["total_area"] = parcels.geometry.area

# Compute spatial intersection between parcel and landuse polygons
overlay = gpd.overlay(parcels, landuse, how="intersection")
overlay["landuse_area"] = overlay.geometry.area

# Compute area % per landuse fragment in each parcel
overlay["percentage"] = (overlay["landuse_area"] / overlay["total_area"]) * 100
overlay["percentage"] = overlay["percentage"].round(2)

# print(overlay.head())

# Print all unique landuse types
# print(landuse["name"].unique())

# Get a list of landuse fragment percentages per parcel (for verification)
mixed_use = overlay.dissolve(
    by="parcel_pin",
    aggfunc={
    "percentage": lambda x: [pct for pct in x],
    "total_area": "first"
})

# Apply classification: find all parcels where no landuse fragment exceeds 60%
mixed_use["is_mixed_use"] = mixed_use["percentage"].apply(lambda x: all([pct < 60 for pct in x]))
mixed_use = mixed_use[mixed_use["is_mixed_use"] == True].copy()

# print(mixed_use.head())

mixed_use = mixed_use.to_crs(epsg=4326)

mixed_use.to_file(
    "output/challenge_result.geojson",
    driver="GeoJSON"
)

print("GeoJSON saved successfully.")