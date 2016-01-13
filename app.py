from flask import Flask, render_template, request
from scripts import mapcalc_kde
import pandas as pd
import numpy as np
import dill

app = Flask(__name__)
# if you're reading this, don't look at the next line. It's SECRET ;)
app.config['SECRET_KEY'] = 'F#$6432fdsY$WTREWgfdassu54agfdsjyt;.,;gfd'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        to_gmap=['new google.maps.LatLng(39.302051282051281, -76.617435897435897)',
                 'new google.maps.LatLng(39.306923076923077, -76.617435897435897)',
                 'new google.maps.LatLng(39.287435897435898, -76.607179487179479)',
                 'new google.maps.LatLng(39.282564102564102, -76.602051282051278)',
                 'new google.maps.LatLng(39.287435897435898, -76.602051282051278)',
                 'new google.maps.LatLng(39.282564102564102, -76.596923076923076)',
                 'new google.maps.LatLng(39.287435897435898, -76.596923076923076)',
                 'new google.maps.LatLng(39.282564102564102, -76.591794871794875)',
                 'new google.maps.LatLng(39.287435897435898, -76.591794871794875)']
        return render_template(
            'index.html',
            to_gmap=to_gmap
        )
    else:
        session=dict()
        session['crime'] = request.form['crime']
        session['vacancy'] = request.form['vacancy']
        session['grocery'] = request.form['grocery']
        session['restaurant'] = request.form['restaurant']
        session['schools'] = request.form['schools']

        # load pre-computed kernel density functions
        crime = dill.load(open('crime.dill', 'r'))
        vacancy = dill.load(open('vacancy.dill', 'r'))
        grocery = dill.load(open('grocery.dill', 'r'))
        restaurant = dill.load(open('restaurant.dill', 'r'))
        schools = dill.load(open('schools.dill', 'r'))

        """This needs to be defined by the google maps api"""

        # Boundary conditions for all maps (longitudes as x vals, latitudes as y vals)
        lonmin = -76.72
        lonmax = -76.52
        latmin = 39.19
        latmax = 39.38

        # number of points along each map edge
        # (total number of points is npts**2)
        npts = 40
        map_threshhold = 0.8

        x = np.linspace(lonmin, lonmax, npts)
        y = np.linspace(latmin, latmax, npts)

        X, Y = np.meshgrid(x, y, indexing='ij')
        grid_points = np.vstack([X.ravel(), Y.ravel()])

        crime_map = mapcalc_kde.kde_map(x, y, crime) * float(session['crime'])
        vacancy_map = mapcalc_kde.kde_map(x, y, vacancy) * float(session['vacancy'])
        grocery_map = mapcalc_kde.kde_map(x, y, grocery) * float(session['grocery'])
        restaurant_map = mapcalc_kde.kde_map(x, y, restaurant) * float(session['restaurant'])
        schools_map = mapcalc_kde.kde_map(x, y, schools) * float(session['schools'])

        map_df = pd.DataFrame({
                'crime':crime_map,
                'vacancy':vacancy_map,
                'grocery':grocery_map,
                'restaurant':restaurant_map,
                'schools':schools_map
            })

        rec_map = map_df.sum(axis=1).values

        to_gmap = mapcalc_kde.produce_google_heatmap_points(rec_map, npts, grid_points, map_threshhold)
        #print 'Value of Crime: '+str(float(session['crime']))
        #print 'Value of vac: '+str(float(session['vacancy']))
        #print 'Value of groc: '+str(float(session['grocery']))
        #print 'Value of school: '+str(float(session['schools']))

        return render_template(
            'index.html',
            to_gmap=to_gmap
        )

if __name__ == '__main__':
    app.run(debug=False)