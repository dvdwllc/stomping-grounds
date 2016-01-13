#!/usr/bin/anaconda/python
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


def compute_kde(POIlons, POIlats, bandwidth):
    """
    Compute a gaussian kernel density estimate for the
    collection of points defined by POIlons and POIlats.

    :param POIlons, POIlats
    list of longitude and latitude coordinates to fit

    :param bandwidth
    bandwidth of the gaussian kernel

    :returns
    scipy.stats.gaussian_kde object
    """
    kernel = gaussian_kde((POIlons, POIlats), bw_method=bandwidth)

    return kernel


def kde_map(lon_vec, lat_vec, kernel):
    """
    Compute the value of the kernel density estimate at each point.

    :param lon_vec. lat_vec
    longitude and latitude vectors defining the map space

    :param kernel
    scipy.stats.gaussian_kde object

    :returns
    len(lon_vec) x len(lat_vec) array of kernel density estimates.
    """
    X, Y = np.meshgrid(lon_vec, lat_vec)

    gridpoints = np.vstack([X.ravel(), Y.ravel()])

    Z = kernel(gridpoints)

    return Z / max(Z)


def gauss_2D(lon_vec, lat_vec, POI_lon, POI_lat, bandwidth):
    """
    Gaussian function for a single point.
    """
    X, Y = np.meshgrid(lon_vec, lat_vec)

    # Bandwidth needs to be related to map size!
    # Or maybe the bandwidth of the other maps...

    gaussian = np.exp(-((X.ravel() - POI_lon) ** 2 +
                        (Y.ravel() - POI_lat) ** 2) / (2 * bandwidth ** 2))

    # print max(gaussian)
    Z = np.reshape(gaussian, X.shape)
    Z = np.rot90(Z).flatten()

    return Z / max(Z)


def plot_KDE(lons, lats, kernel_density, mapname):
    plt.figure(figsize=(6, 5))
    plt.imshow(
        np.rot90(np.reshape(kernel_density, (len(lons), len(lats))).T),
        cmap=plt.cm.gist_earth_r,
        extent=[min(lons), max(lons), min(lats), max(lats)]
    )
    plt.axis([min(lons), max(lons), min(lats), max(lats)])
    plt.title(mapname)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Kernel Density (arb.)')

def produce_google_heatmap_points(rec_map, npts, gridpoints, match_tolerance):
    mapmax = np.max(rec_map)
    top_spots = np.argwhere(np.reshape(rec_map, (npts, npts)).T.flatten() > mapmax * match_tolerance)
    best_lat_lng = zip([gridpoints.T[i,1][0] for i in top_spots], [gridpoints.T[i,0][0] for i in top_spots])
    goog_map_points = []
    for i in best_lat_lng:
        goog_map_points.append('new google.maps.LatLng'+str(i))
    return goog_map_points
