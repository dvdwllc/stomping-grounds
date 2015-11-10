__author__ = 'wallacdc'

import geocoder
import numpy as np


def add_user_POI(address):
    """
    Converts the address for a Point of Interest to longitude and latitude
    coordinates and saves the coordinates in the user_POIs dictionary.

    :param address:
        Address of the POI
    :return:
        1 if successfully added POI coordinates
        0 if unsuccessful
    """
    g = geocoder.arcgis(address)
    if len(g.latlng) > 0:
        return np.array([g.latlng])
    else:
        print 'Invalid address or geocode failure!'
        return 0