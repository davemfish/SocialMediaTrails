""""
This is a saved model run from natcap.invest.recreation.recmodel_client.
Generated: 09/14/17 11:21:55
InVEST version: 3.3.3
"""
import natcap.invest.recreation.recmodel_client


def main():
    #specify directory
    #scan and save all shapefile (.shp) file names in directory
    #iterate over list of all shapefiles (aoi's) and call invest rec model
    #output naming convention, includes order in name

    args = {
        u'aoi_path': u'C:/Users/Matt Dunbar/Documents/PythonProjects/SocialMediaTrails/matt/AOI_Files/GlacierNP_AlbersCONUS.shp',
        u'cell_size': 700.0,
        u'compute_regression': False,
        u'end_year': u'2014',
        u'grid_aoi': True,
        u'grid_type': u'hexagon',
        u'results_suffix': 'GlacierNP_2005_2014_700',
        u'start_year': u'2005',
        u'workspace_dir': u'C:\\Users\\Matt Dunbar\\Documents\\PythonProjects\\SocialMediaTrails\\matt\\OUTPUT',
    }

    natcap.invest.recreation.recmodel_client.execute(args)

if __name__ == '__main__':
    main()

