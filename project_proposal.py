
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data collected from baltimore city open data project
vacancies = pd.read_csv('vacancies/Vacant_Buildings.csv')
arrests = pd.read_csv('arrests/BPD_Arrests.csv')

# Clean location data in arrests dataframe
lat = np.zeros(len(arrests['Location 1']))
lon = np.zeros(len(arrests['Location 1']))

for i in range(len(arrests['Location 1'])):
    try:
        lat[i], lon[i] = tuple(map(float, arrests['Location 1'][i].strip('()').split(',')))
    except AttributeError:
        lat[i], lon[i] = np.nan, np.nan

arrests['latitude'] = pd.Series(lat)
arrests['longitude'] = pd.Series(lon)
arrests = arrests[pd.notnull(arrests['longitude'])]


# Get all offenses in the dataframe
all_offenses = arrests.groupby('IncidentOffense').count().index.values

def offense_query(offense):
    """Query the arrests database for a specific offense"""
    try:
        rows = arrests['IncidentOffense'].str.contains(offense)
    except KeyError:
        return 0
    return rows


def plot_offense_map(offense, cl, darkness):
    """Generate a heatmap of a particular offense in the city"""
    rows = arrests['IncidentOffense'].str.contains(offense)
    lats, longs = arrests[rows]['latitude'], arrests[rows]['longitude']
    plt.plot(longs, lats, '.', color=cl, alpha=darkness, label=offense)


# For fun, plot a heatmap of vacant homes and prostitution arrests
plt.figure(figsize=(5.5,5))
plt.plot(vacancies['Location2'],
         vacancies['Location 1'],
         '.',
         color='black',
         alpha=0.1, label='Vacant Homes')
plot_offense_map("Prostitution", "red", 1)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Vacant Homes and Prostitution Arrests in Baltimore (2014)')
plt.ylabel('Latitude (degrees)')
plt.xlabel('Longitude (degrees)')
plt.show()
# Bin the vacancies data or arrests data for a given offense
# so we can see correlations between different types of crime
# by area

nbins = 50
def hist2d_bmoredata(longcol, latcol, plot=True, masked=True, edges=False):
    """
    Generate a location-based 2D histogram from a given dataset.

    :param longcol: array containing longitude coordinates in degrees
    :param latcol: array containing latitude coordinates in degrees
    :param plot: Boolean. shows a plot of the 2D histogram if True.
    :param masked: Boolean. Whether or not to mask empty bins
    :param edges: Boolean. Whether or not to return bin edge arrays.
    :return:
        if edges: xedges array, yedges array, nbins by nbins array
                    of counts vs. location
        if masked: nbins by nbins array of counts vs. location with
                    zero vals masked
        else: nbins*nbins array of counts
    """
    maprange = np.array([(-76.75, -76.5), (39.20, 39.38)])

    H, xedges, yedges = np.histogram2d(longcol,
                                       latcol,
                                       bins=nbins,
                                       range=maprange)

    # H needs to be rotated and flipped
    H = np.rot90(H)
    H = np.flipud(H)

    # Mask zeros
    Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero

    if plot:
        # Plot 2D histogram using pcolor
        fig2 = plt.figure(figsize=(6,5))
        plt.pcolormesh(xedges,yedges,Hmasked)
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Counts')

    if edges:
        return xedges, yedges, H

    if masked:
        return Hmasked.flatten()
    else:
        return H.flatten()

# get the edges so we can make plots
all_arrests = hist2d_bmoredata(arrests['longitude'], arrests['latitude'], 0, 0, 0)
xedges, yedges, _ = hist2d_bmoredata(vacancies['Location2'],
                                     vacancies['Location 1'],
                                     False,
                                     False,
                                     True)

def arrest_histogram(offense):
    """Generate a 1D array of arrests vs. location for a given offense"""
    rows = offense_query(offense)
    lats, longs = arrests[rows]['latitude'], arrests[rows]['longitude']
    try:
        offenses = hist2d_bmoredata(longs, lats, False, False, False)
    except KeyError:
        return 0

    return np.array(offenses)

#####Principal Component Analysis of Offenses#######


# Let's just look at the top 9 offenses, which are responsible for the vast
# majority of all arrests.
offenses2plot = ('Narcotics', 'Ass', 'Larceny',
                 'Disorderly','Burg', 'Prostitution',
                 'Trespassing', 'Destruct', 'Robb')

# Get 1D arrays of counts vs. location for all offenses.
offense_histograms = []
for i in range(len(offenses2plot)):
    offense_histograms.append(arrest_histogram(offenses2plot[i]))

# Make a dataframe from all 1D offense arrays
offense_histograms = pd.DataFrame(offense_histograms).T

# Only nonzero boxes are included in the PCA
real_indices = all_arrests != 0
offense_histograms = offense_histograms[real_indices]
offense_histograms.columns = (offenses2plot)

# For PCA, all data must have zero mean. Subtract the sample mean from each set
means = np.mean(offense_histograms, axis=0)
crime_0 = offense_histograms-means
crime_0.columns = (offenses2plot)

(N, M) = crime_0.shape
covariance = (1.0/(N-1.0))*crime_0.T.dot(crime_0) # Covariance matrix
L, E = np.linalg.eig(covariance) # Eigenvalues, Eigenvectors
E1, E2, E3, E4 = crime_0.dot(E[:4].T) # First 3 eigenvectors


# Scree plot to view the contribution of all eigenvectors
plt.figure(2)
plt.title('Scree Plot of Eigenvalues')
plt.xlabel('Eigenvalue number')
plt.ylabel('Fractional contribution to total')
plt.plot(np.cumsum(L)/np.cumsum(L)[-1])
plt.show()

# Project all crime onto the first four eigenvectors
reduced_crime = crime_0.dot(E[:4].T)

# Now we can get view the "density" of each crime vector as a
# function of location!
E1_vals, E2_vals, E3_vals, E4_vals = np.zeros((4,len(all_arrests)))
for i in range(len(all_arrests)):
    if all_arrests[i] != 0:
        E1_vals[i], E2_vals[i], E3_vals[i], E4_vals[i] = \
        reduced_crime[0][i], reduced_crime[1][i], reduced_crime[2][i], reduced_crime[3][i]

# First eigenvector with zeros masked
E1_masked_map = -np.ma.masked_where(E1_vals==0, E1_vals).reshape(nbins,nbins)

# Plot a heatmap of the first crime vector
plt.figure(3)
plt.pcolormesh(xedges,yedges,E1_masked_map)
cbar = plt.colorbar()
cbar.ax.set_ylabel('Crime Level')
plt.title('First Crime Eigenvector')
plt.ylabel('Latitude (degrees)')
plt.xlabel('Longitude (degrees)')
plt.show()
