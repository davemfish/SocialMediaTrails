""""
This is a saved model run from natcap.invest.recreation.recmodel_client.
Generated: 09/14/17 11:21:55
InVEST version: 3.3.3
"""
import os
import natcap.invest.recreation.recmodel_client

def main():

    folder = 'AOI_Files'
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.shp'):
            print(os.path.join(folder, file))
            # get bounding box, determine cell size
            # geopandas read shapefiles into geodataframe
            # use bounding box method
            # math to determine max (width/height)
            # math to divide max by fixed number of cells desired...giving cell size
            # setup args : modify aoi_path, cell size, results_suffix

            # run natcap with args

    args = {
        u'aoi_path': u'C:/Users/Matt Dunbar/Documents/PythonProjects/SocialMediaTrails/matt/AOI_Files/SingleParkByRank/All_NPS_Park_Bounds_Ranked_Rank_01.shp',
        u'cell_size': 700.0,
        u'compute_regression': False,
        u'end_year': u'2014',
        u'grid_aoi': True,
        u'grid_type': u'hexagon',
        u'results_suffix': '01_700_2005_2014',
        u'start_year': u'2005',
        u'workspace_dir': u'C:\\Users\\Matt Dunbar\\Documents\\PythonProjects\\SocialMediaTrails\\matt\\OUTPUT',
    }

    natcap.invest.recreation.recmodel_client.execute(args)


if __name__ == '__main__':
    main()

