import mapcalc_kde
import pandas as pd
import numpy as np
import dill

class StaticMapConstructor(object):
    """
    Constructs static kernel density maps from csv files 
    containing Latitude, Longitude coordinates.
    
    Assumes data is for Baltimore City. If not, need to change 
    lat min/max and lon min/max bounding box!
    """
    
    def __init__(self, n_grid_pts, kernel_bandwidth, file_dict):
        self.n_grid_pts = n_grid_pts
        self.kernel_bandwidth = kernel_bandwidth
        self.keys = []
        self.dataframes = []
        for key in file_dict:
            self.keys.append(key)
            self.dataframes.append(pd.read_csv(file_dict[key]))
            
    def compute_KDEs(self):
        self.KDEs = []
        for i in range(len(self.keys)):
            df = self.dataframes[i]
            KDE = mapcalc_kde.compute_kde(df['Longitude'], 
                                             df['Latitude'], 
                                             kernel_bandwidth)
            self.KDEs.append(KDE)
            
    def construct_maps(self):
        self.total_map = pd.DataFrame()
        # Boundary conditions for all maps (longitudes as x vals, latitudes as y vals)
        lonmin = -76.72
        lonmax = -76.52
        latmin = 39.19
        latmax = 39.38

        # number of points along each map edge
        # (total number of points is npts**2)
        npts = 200

        x = np.linspace(lonmin, lonmax, npts)
        y = np.linspace(latmin, latmax, npts)

        X, Y = np.meshgrid(x, y, indexing='ij')
        positions = np.vstack([X.ravel(), Y.ravel()])
        
        for i in range(len(self.keys)):
            self.total_map[self.keys[i]] = mapcalc_kde.kde_map(x, y, self.KDEs[i])
            
    def dump_full_map(self, filename):
        dill.dump(self.total_map, open(filename, 'w'))