# SocialMediaTrails

### data/
pud_results_hex.shp -- this a sample output of the InVEST Recreation model. Use this shapefile to protoype a plotting function that symbolizes the "PUD_YR_AVG" attribute, to display relative visitation rates across the polygons.

rainierNP_boundary.shp -- this is simply a polygon boundary of Mt Rainier National Park. It could be used as an input to the InVEST Rec model.

### scripts/
userdays.r -- an example of how the raw Flickr point data is processed into metrics of photo-user-days. We probably won't need to use this script since that same functionality is built into InVEST 

recmodel_client_parameters_boilerplate.py -- a python script that calls the InVEST Rec model by importing natcap.invest. natcap.invest can be installed with pip (`pip install natcap.invest`). More details on installing dependencies here: https://pypi.python.org/pypi/natcap.invest


## Goals (in no particular order)

- use geopandas to script a workflow that reads the pud_results output of InVEST and maps the "PUD_YR_AVG" variable.

- Run the InVEST Rec model from a python script, using the rainier boundary as the input 'Area of Interest', and use the 'grid_aoi' parameter to have InVEST divide the boundary into square or hexagonal grid cells. 

- expand on the previous two scripts by coding a workflow that takes the boundary of each National Park in the US, runs the invest model to generate gridded PUD values for each park, and use geopandas to make a series of maps, one for each park.
