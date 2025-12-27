# Polygon Cleaning and Processing Project

## My Approach

**This project cleans and processes a shapefile of building polygons to prepare them for spatial analysis. The main steps are:**

1. **Data Inspection**: Load and explore the polygon shapefile.
2. **Validation**: Make sure all polygon geometries are valid.
3. **Area Calculation**: Compute a correct area for each polygon.
4. **Noise Removal**: Remove very small polygons (less than 1% of the largest area).
5. **Simplification**:Reduce jagged edges by simplifying the geometry.
6. **Corner Smoothing**: Round sharp corners using buffering.
7. **Hole Removal**: Remove small internal holes while keeping meaningful ones.

The workflow keeps the topology intact and improves polygon quality for later spatial analysis.

## Libraries Used

* `geopandas`: For working with shapefiles and GeoDataFrames.
* `shapely`: For geometry operations like validation, simplification, and buffering.
* `matplotlib.pyplot`: To visualize polygons.
* `numpy`: For numerical operations.
* `warnings`:  To suppress unnecessary warnings.

## How to Run the Code

1. **Install dependencies**:

   ```bash
   pip install geopandas shapely matplotlib numpy
   ```

2. **Update the file path** in the notebook:

   * Replace `"C:\\Users\\DELL\\AssessmentTask\\test.shp"` with your shapefile path.

3. **Run the notebook** step by step:

   * Import libraries.
   * Load your shapefile.
   * Execute the cleaning steps (validation, area calculation, filtering, simplification, etc.).
   * Visualize the results using `matplotlib`.

4. **Output**:

   * The cleaned polygons are stored in the `polygon` GeoDataFrame.
   * The final plot shows the smoothed and simplified polygons.

