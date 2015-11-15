#!/usr/bin/anaconda/python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Boundary conditions for all maps (longitudes as x vals, latitudes as y vals)
lonmin = -76.72
lonmax = -76.52
latmin = 39.19
latmax = 39.38

# number of points along each map edge
# (total number of points is npts**2)
npts = 60

x = np.linspace(lonmin, lonmax, npts)
y = np.linspace(latmin, latmax, npts)

city_limits = np.array([(39.371582, -76.711036), (39.370668, -76.529172),
                        (39.209645, -76.529172), (39.196875, -76.549085),
                        (39.206985, -76.584790), (39.232519, -76.610883),
                        (39.278245, -76.710446), (39.371582, -76.711036)])


def compute_distances_to_POIs(POIs):
    """
    Computes the distance to the nearest Point Of Interest (POI)
    for every point in the npts x npts grid of latitudes and longitudes.

    :param POIs:
        2xn array of latitudes and longitudes of each POI
        -or-
        Pandas dataframe containing 'Latitude' and 'Longitude' columns for
        each POI

    :return:
        npts x npts array of distance to nearest POI

    """
    # get POI's
    try:
        # if coordinates as arrays
        lons, lats = POIs[:, 1], POIs[:, 0]
    except TypeError:
        # if coordinates in pandas dataframe
        lons, lats = POIs['Longitude'].values, POIs['Latitude'].values

    # initialize distances to large values
    mindists = 100.0 * np.ones((npts, npts))

    # iterate through all points in lat/lon grid
    for i in range(len(x)):  # iterate through longitudes
        for j in range(len(y)):  # iterate through latitudes
            for k in range(len(POIs)):  # find closest POI in array
                dist = np.hypot((x[i] - lons[k]), (y[j] - lats[k]))
                if dist < mindists[j][i]:
                    mindists[j][i] = dist  # save distance to closes POI
    return mindists


def plot_distances_to_POIs(mindists, POIs=[]):
    """
    Plots a 2D heatmap of distance to nearest POI.

    :param mindists:
     npts by npts array of distances to nearest POI
    :param POIs:
     2xn array of latitudes and longitudes of each POI
     -or-
     Pandas dataframe containing 'Latitude' and 'Longitude' columns for
     each POI
    :return:
     1
    """

    plt.figure(figsize=(5, 5))
    plt.axis([lonmin, lonmax, latmin, latmax])
    plt.pcolormesh(x, y, mindists)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.plot(city_limits[:, 1], city_limits[:, 0], color='red')

    if len(POIs) != 0:  # get POI's
        try:
            # if coordinates as arrays
            lons, lats = POIs[:, 1], POIs[:, 0]
        except TypeError:
            # if coordinates in pandas dataframe
            lons, lats = POIs['Longitude'].values, POIs['Latitude'].values

        plt.plot(lons, lats, 'x', color='red')

    return x, y, mindists


def produce_map_for_app(mindists):
    """
    Plots a 2D heatmap of distance to nearest POI.

    :param mindists:
     npts by npts array of distances to nearest POI
    :return:
     x, y, mindists
    """

    return x, y, mindists


def hist2d_bmoredata(POIs, plot=True, masked=True):
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

    H, _, _ = np.histogram2d(lons, lats, bins=npts, range=maprange)

    # H needs to be rotated and flipped
    H = np.rot90(H)
    H = np.flipud(H)

    if plot:
        # Plot 2D histogram using pcolor
        fig2 = plt.figure(figsize=(6, 5))
        plt.pcolormesh(x, y, H)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Counts (arb.)')

    if masked:
        # Mask zeros
        Hmasked = np.ma.masked_where(H == 0, H)  # Mask pixels with a value of zero
        return Hmasked
    else:
        return H
