from flask import Flask, render_template
import ee
import geemap

# Initialize Flask app
app = Flask(__name__)

# Authenticate and initialize Earth Engine
ee.Initialize()

# Initialize geemap map
Map = geemap.Map()

# Define Region of Interest (India)
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
roi = countries.filter(ee.Filter.eq("country_na", "India"))
Map.addLayer(roi, {}, "India")
Map.centerObject(roi, 8)

# Filter methane data by date and region
Methane = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4") \
    .filterDate('2016-01-01', '2017-01-01') \
    .filterBounds(roi)

# Filter carbon monoxide data by date and region
CO = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO") \
    .filterDate('2016-01-01', '2017-01-01') \
    .filterBounds(roi)

# Create composites by taking the median value for both gases
methaneComposite = Methane.median()
coComposite = CO.median()

# Define visualization parameters for methane
methaneVis = {
    'bands': ["CH4_column_volume_mixing_ratio_dry_air"],
    'min': 1750,
    'max': 1900,
    'palette': ['blue', 'green', 'yellow', 'orange', 'red']
}

# Define visualization parameters for carbon monoxide
coVis = {
    'bands': ["CO_column_number_density"],
    'min': 0.03,
    'max': 0.05,
    'palette': ['purple', 'blue', 'cyan', 'green', 'yellow', 'red']
}

# Add methane and carbon monoxide composite layers to the map
Map.addLayer(methaneComposite.clip(roi), methaneVis, "Methane RGB")
Map.addLayer(coComposite.clip(roi), coVis, "Carbon Monoxide RGB")

@app.route("/")
def index():
    # Save the map as an HTML file
    Map.to_html("templates/map.html")
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
import ee
import geemap

# Initialize Flask app
app = Flask(__name__)

# Initialize Earth Engine
ee.Initialize()

# Initialize geemap map
Map = geemap.Map()

# Define Region of Interest (India)
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
roi = countries.filter(ee.Filter.eq("country_na", "India"))
Map.addLayer(roi, {}, "India")
Map.centerObject(roi, 8)

# Filter methane data by date and region
Methane = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4") \
    .filterDate('2016-01-01', '2017-01-01') \
    .filterBounds(roi)

# Filter carbon monoxide data by date and region
CO = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO") \
    .filterDate('2016-01-01', '2017-01-01') \
    .filterBounds(roi)

# Create composites by taking the median value for both gases
methaneComposite = Methane.median()
coComposite = CO.median()

# Define visualization parameters for methane
methaneVis = {
    'bands': ["CH4_column_volume_mixing_ratio_dry_air"],
    'min': 1750,
    'max': 1900,
    'palette': ['blue', 'green', 'yellow', 'orange', 'red']
}

# Define visualization parameters for carbon monoxide
coVis = {
    'bands': ["CO_column_number_density"],
    'min': 0.03,
    'max': 0.05,
    'palette': ['purple', 'blue', 'cyan', 'green', 'yellow', 'red']
}

# Add methane and carbon monoxide composite layers to the map
Map.addLayer(methaneComposite.clip(roi), methaneVis, "Methane RGB")
Map.addLayer(coComposite.clip(roi), coVis, "Carbon Monoxide RGB")

@app.route("/")
def index():
    # Save the map as an HTML file
    Map.to_html("static/map.html")
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)
