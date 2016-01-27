#!/usr/bin/anaconda/python
#import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
#import matplotlib.pyplot as plt


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

    return Z / np.std(Z)


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
    """
    Plot a heatmap map of estimated kernel density.
    
    kernel_density is an npts**2 array and needs to be reshaped according
    to the provided lon, lat coordinates.
    """
    # transform the kernel to the correct dimensions and orientation
    transformed_kernel = np.rot90(np.reshape(kernel_density, (len(lons), len(lats))).T)
    
    # show the computed kernel density as an image
    # extent sets the boundaries of the image
    plt.figure(figsize=(5,4.5))
    plt.imshow(
        transformed_kernel,
        cmap=plt.cm.RdBu,
        extent=[min(lons), max(lons), min(lats), max(lats)]
    )
    
    # set plot details
    plt.axis([min(lons), max(lons), min(lats), max(lats)])
    plt.title(mapname)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Kernel Density (arb.)')

def produce_google_heatmap_points(rec_map, npts, gridpoints, match_tolerance):
    """
    Add docstring.
    
    Fix threshold function.
    
    Add ability to reduce number of points dynamically (if recommended area is large)
    """
    mapmax = np.max(rec_map)
    top_spots = np.argwhere(np.reshape(rec_map, (npts, npts)).T.flatten() > mapmax * match_tolerance)
    best_lat_lng = zip([gridpoints.T[i,1][0] for i in top_spots], [gridpoints.T[i,0][0] for i in top_spots])
    goog_map_points = []
    for i in best_lat_lng:
        goog_map_points.append('new google.maps.LatLng'+str(i))
    return goog_map_points
