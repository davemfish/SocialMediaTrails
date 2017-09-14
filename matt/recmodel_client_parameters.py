""""
This is a saved model run from natcap.invest.recreation.recmodel_client.
Generated: 09/14/17 11:21:55
InVEST version: 3.3.3
"""

import natcap.invest.recreation.recmodel_client


args = {
        u'aoi_path': u'C:/Users/Matt Dunbar/Documents/PythonProjects/SocialMediaTrails/matt/AOI_Files/GlacierNP_AlbersCONUS.shp',
        u'cell_size': 7000.0,
        u'compute_regression': False,
        u'end_year': u'2014',
        u'grid_aoi': True,
        u'grid_type': u'hexagon',
        u'results_suffix': 'GlacierNP_2005_2014',
        u'start_year': u'2005',
        u'workspace_dir': u'C:\\Users\\Matt Dunbar\\Documents\\PythonProjects\\SocialMediaTrails\\matt\\OUTPUT',
}

if __name__ == '__main__':
    natcap.invest.recreation.recmodel_client.execute(args)
