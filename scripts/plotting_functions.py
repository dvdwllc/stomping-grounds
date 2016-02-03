import matplotlib.pyplot as plt
import numpy as np

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