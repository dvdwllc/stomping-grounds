#!/usr/bin/anaconda/python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# Boundary conditions for all maps (longitudes as x vals, latitudes as y vals)
lonmin = -76.72
lonmax = -76.52
latmin = 39.19
latmax = 39.38

# number of points along each map edge
# (total number of points is npts**2)
npts = 100

x = np.linspace(lonmin, lonmax, npts)
y = np.linspace(latmin, latmax, npts)

city_limits = np.array([(39.371582, -76.711036), (39.370668, -76.529172),
                        (39.209645, -76.529172), (39.196875, -76.549085),
                        (39.206985, -76.584790), (39.232519, -76.610883),
                        (39.278245, -76.710446), (39.371582, -76.711036)])


# Boundary conditions for all maps (longitudes as x vals, latitudes as y vals)
lonmin = -76.72
lonmax = -76.52
latmin = 39.19
latmax = 39.38

# number of points along each map edge
# (total number of points is npts**2)
npts = 30

x = np.linspace(lonmin, lonmax, npts)
y = np.linspace(latmin, latmax, npts)

def kde_map(POIs, plot=True):
    """
    Produces a npts x npts histogram from an array of longitudes and latitudes.

    :param POIs:
        2xn NumPy array of locations
        -or-
        Pandas dataframe containing 'Longitude' and 'Latitude' columns
    :param plot:
        Boolean - if True, produces a plot of the resulting histogram
    :param masked:
        Boolean - if True, returns a masked array (zeros are masked)
    :return:
        npts x npts NumPy array (2D histogram)
    """
    # get POI's
    try:
        # if coordinates as arrays
        lons, lats = POIs[:, 1], POIs[:, 0]
    except TypeError:
        # if coordinates in pandas dataframe
        lons, lats = POIs['Longitude'].values, POIs['Latitude'].values

    maprange = np.array([(lonmin, lonmax), (latmin, latmax)])

    kernel = gaussian_kde((lons, lats))

    X, Y = np.meshgrid(x, y)
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kernel(positions), X.shape)

    # correct orientation of kernel density estimate
    Z = np.rot90(Z.T)

    if plot:
        # Plot KDE
        plt.figure(figsize=(6, 5))
        plt.plot(lons, lats, 'k.', markersize=1, alpha=1)
        plt.imshow(Z,
                   cmap=plt.cm.gist_earth_r,
                   extent=[lonmin, lonmax, latmin, latmax]
                    )
        plt.axis([lon1, lon2, lat1, lat2])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Kernel Density (arb.)')

    return Z

def produce_map_for_app(mindists):
	"""
    Plots a 2D heatmap of distance to nearest POI.

    :param mindists:
     npts by npts array of distances to nearest POI
    :return:
     x, y, mindists
    """

	return x, y, mindists