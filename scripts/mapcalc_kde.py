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
npts = 30

x = np.linspace(lonmin, lonmax, npts)
y = np.linspace(latmin, latmax, npts)

X, Y = np.meshgrid(x, y)
positions = np.vstack([X.ravel(), Y.ravel()])

def kde_map(lon_vec, lat_vec, POIlons, POIlats):
    """
    Gaussian KDE for vectors of points.
    """
    X, Y = np.meshgrid(lon_vec, lat_vec)
    gridpoints = np.vstack([X.ravel(), Y.ravel()])

    kernel = gaussian_kde((POIlons, POIlats))

    Z = np.reshape(kernel(gridpoints), X.shape)

    # correct orientation of kernel density estimate
    Z = np.rot90(Z.T)

    return Z / max(Z.flatten())

def gauss_2D(lon_vec, lat_vec, POI_lon, POI_lat, bandwidth):
    """
    Gaussian function for a single point.
    """
    X, Y = np.meshgrid(lon_vec, lat_vec)

    # Bandwidth needs to be related to map size!
    # Or maybe the bandwidth of the other maps...

    gaussian = np.exp(-((X.ravel()-POI_lon)**2 +
                        (Y.ravel()-POI_lat)**2)/(2*bandwidth**2))

    #print max(gaussian)
    Z = np.reshape(gaussian, X.shape)
    Z = np.rot90(Z.T)

    return Z

def plot_KDE(lons, lats, kernel_density, mapname):
    plt.figure(figsize=(6, 5))
    plt.imshow(
        kernel_density,
        cmap=plt.cm.gist_earth_r,
        extent=[min(lons), max(lons), min(lats), max(lats)]
              )
    plt.axis([min(lons), max(lons), min(lats), max(lats)])
    plt.title(mapname)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Kernel Density (arb.)')

