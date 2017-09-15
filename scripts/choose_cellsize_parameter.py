## a helper function for the recmodel_client.

## see recmodel_client_parameters_boilerplate.py for usage

import os
from osgeo import ogr
from osgeo import gdal
from osgeo import osr
import shapely
import shapely.geometry
import shapely.wkt

def choose_cellsize(shp_path, ncells):
	'''
	Inputs:
	shp_path : string : filepath to shapefile
	ncells : integer : number of cells for each row of the long 
	dimension of the shapefile's bounding box.

	Outputs:
	float : cell length in units that match the aoi CRS.
	'''
	vector = ogr.Open(shp_path)
	vector_layer = vector.GetLayer()
	spat_ref = vector_layer.GetSpatialRef()

	original_vector_shapes = []
	for feature in vector_layer:
	    wkt_feat = shapely.wkt.loads(feature.geometry().ExportToWkt())
	    original_vector_shapes.append(wkt_feat)
	vector_layer.ResetReading()

	extent = vector_layer.GetExtent()  # minx maxx miny maxy

	width = extent[1] - extent[0]
	height = extent[3] - extent[2]
	if width > height:
	    cs = width/ncells
	else:
	    cs = height/ncells
	return(cs)

