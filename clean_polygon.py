import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# Configuration
INPUT_PATH = r"C:\Users\DELL\AssessmentTask\test.shp"
OUTPUT_PATH_SHP = r"C:\Users\DELL\AssessmentTask\test_cleaned.shp"
OUTPUT_PATH_GEOJSON = r"C:\Users\DELL\AssessmentTask\test_cleaned.geojson"

# Load data 
polygon = gpd.read_file(INPUT_PATH)

# Clean polygons 
polygon["geometry"] = polygon["geometry"].apply(make_valid)
polygon["Area"] = polygon.geometry.area

# Remove very small polygons
min_area = polygon["Area"].max() * 0.005
polygon = polygon[polygon["Area"] >= min_area]

# Simplify geometries
tolerance = 1.3
polygon["geometry"] = polygon.geometry.simplify(tolerance, preserve_topology = True)

# Smooth sharp corners
buffer_size = 0.5
polygon["geometry"] = polygon.geometry.buffer(buffer_size).buffer(-buffer_size)

# Remove tiny holes
min_hole_area = 0.01 * polygon["Area"].max()

def remove_tiny_holes(poly):
    if poly.is_empty or poly.geom_type != "Polygon":
        return poly
    large_holes = [h for h in poly.interiors if Polygon(h).area >= min_hole_area]
    return Polygon(poly.exterior, holes=large_holes)

polygon["geometry"] = polygon["geometry"].apply(remove_tiny_holes)
polygon = polygon.reset_index(drop = True)

# Merge polygons by index 
def merge_polygons(gdf, indices, buffer_dist = 1.0, keep_largest = True):
    to_merge = gdf.loc[indices]
    to_keep = gdf.drop(indices)
    merged_geom = unary_union(to_merge.geometry.buffer(buffer_dist)).buffer(-buffer_dist)
    
    if merged_geom.geom_type == "MultiPolygon" and keep_largest:
        merged_geom = max(merged_geom.geoms, key = lambda g: g.area)
    
    merged_row = gpd.GeoDataFrame(
        {"geometry": [merged_geom], "Area": [merged_geom.area]},  crs = gdf.crs)
    return pd.concat([to_keep, merged_row], ignore_index=True)

# Perform merges
polygon = merge_polygons(polygon, [1, 4, 10, 2], buffer_dist = 2.0)
polygon = merge_polygons(polygon, [2, 4, 0], buffer_dist = 1.0)

# Save outputs
polygon.to_file(OUTPUT_PATH_SHP)
polygon.to_file(OUTPUT_PATH_GEOJSON, driver = "GeoJSON")

# Plot before vs after 
original = gpd.read_file(INPUT_PATH)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 8))

original.plot(ax = ax1, color = "pink", edgecolor = "black", linewidth=0.5)
ax1.set_title(f"Before: {len(original)} polygons")

polygon.plot(ax = ax2, color = "lightblue", edgecolor = "black", linewidth=0.5)
ax2.set_title(f"After: {len(polygon)} polygons")

plt.tight_layout()
plt.show()