""""
This is a saved model run from natcap.invest.recreation.recmodel_client.
Generated: Mon 28 Nov 2016 09:24:28 AM 
InVEST version: 3.3.1b1.post10+nff1c8fdca089
"""

import natcap.invest.recreation.recmodel_client
# natcap.invest source code available here:
# https://bitbucket.org/natcap/invest/
from choose_cellsize_parameter import choose_cellsize

aoi = '../data/rainierNP_boundary.shp'

# 'aoi_path' and 'workspace_dir' are required arguments
args = {
        u'aoi_path': aoi, # path to a shapefile
        u'grid_aoi': True,
        u'grid_type': u'hexagon',
        u'cell_size': 7000.0,
        u'start_year': u'2005',
        u'end_year': u'2014',
        u'compute_regression': False,
        u'predictor_table_path': u'',
        u'scenario_predictor_table_path': u'',  
        u'results_suffix': u'',
        u'workspace_dir': u'../dave/test_invest', # path to a directly 
}

cs = choose_cellsize(aoi, 100)
args['cell_size'] = cs
print(args)

if __name__ == '__main__':
    natcap.invest.recreation.recmodel_client.execute(args)
