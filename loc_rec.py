import pandas as pd
import sqlite3
import numpy as np
from sqlalchemy import create_engine
from scripts import mapcalc, get_user_POIs
import geocoder

# Initializes database with filename baltimore.db in current directory
disk_engine = create_engine('sqlite:///baltimore.db') 

class recommender(object):
    
    def __init__(self, queries): 
        self.queries = queries
        self.n_queries = len(self.queries)
        self.maps = []
        print 'there are %i queries' % self.n_queries
        
    def compute_maps(self):
        for i in range(self.n_queries):
            q = self.queries[i]
            if type(q) == tuple:
                print 'query %i is a tuple' % i
                if q[0] == 'arrests':
                    print 'query %i is arrests' % i
                    result = \
                    pd.read_sql_query('SELECT Latitude, Longitude FROM {} '
                                      'WHERE {} = "{}"'.format(q[0], q[1], q[2])
                                      , disk_engine)
                    self.maps.append(\
                    mapcalc.hist2d_bmoredata(result, 0, 0) + 1.0)
                    print 'appended map %i' % i
                else:
                    print 'query %i is not arrests' % i
                    result = \
                    pd.read_sql_query('SELECT Latitude, Longitude FROM {} '
                                      'WHERE {} = "{}"'.format(q[0], q[1], q[2])
                                      , disk_engine)
                    self.maps.append(mapcalc.compute_distances_to_POIs(result))
                    print 'appended map %i' % i
                 
            else:
                print 'query %i is not a tuple' % i
                # If no identifier column to choose from
                if q == 'vacancies' or q == 'restaurants':
                    print 'query %i is vacancies or restaurants' % i
                    result = \
                    pd.read_sql_query('SELECT Latitude, Longitude '
                    				  'FROM vacancies '
                                      , disk_engine)
                    self.maps.append(mapcalc.hist2d_bmoredata(result, 0, 0)+1.0)
                    print 'appended map %i' % i
                    
                else:
                    print 'query %i is an address' % i
                    result = get_user_POIs.add_user_POI(q)
                    try:
                      self.maps.append\
                      	(mapcalc.compute_distances_to_POIs(result))
                    except TypeError as e:
                        print 'appended map %i' % i
                    # print 'Failed to geocode manually entered location.\n'
                    
    
    def recommend_location(self):
        map_array = np.array(self.maps)
        heatmap = np.prod((1.0 / map_array), axis=0)
        print '%i out of %i heatmaps were included' % \
        				(len(map_array), self.n_queries, )
        return heatmap
   
if __name__ == '__main__':
	import matplotlib.pyplot as plt
	JHU = ('3400 N Charles St, Baltimore, MD')
	q1 = 'groceries', 'type', 'Full Supermarket'
	q2 = 'arrests', 'Offense', '87-Narcotics'
	q3 = 'vacancies'    
	my_spot = recommender([JHU,q1,q2,q3])
	my_spot.compute_maps()
	loc_map = my_spot.recommend_location()
	mapcalc.plot_distances_to_POIs(loc_map)
	plt.show() 
