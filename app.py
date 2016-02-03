from flask import Flask, render_template, request
from scripts import mapcalc_kde
import pandas as pd
import numpy as np
import dill

app = Flask(__name__)
# if you're reading this, don't look at the next line. It's SECRET ;)
#app.config['SECRET_KEY'] = 'F#$6432fdsY$WTREWgfdassu54agfdsjyt;.,;gfd'

@app.route('/', methods=['GET','POST'])
def index():
    # on initial landing, show the default heatmap
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
        # user-defined weights for each map
        session=dict()
        session['crime'] = float(request.form['crime'])
        session['vacancy'] = float(request.form['vacancy'])
        session['grocery'] = float(request.form['grocery'])
        session['restaurant'] = float(request.form['restaurant'])
        session['schools'] = float(request.form['schools'])
        session['museums'] = float(request.form['museums'])
        session['parks'] = float(request.form['parks'])
        session['liquor'] = float(request.form['liquor'])
        session['libraries'] = float(request.form['libraries'])

        # weights as an array
        multipliers = np.array([
            session['crime'],
            session['vacancy'],
            session['grocery'],
            session['restaurant'],
            session['schools'],
            session['museums'],
            session['parks'],
            session['liquor'],
            session['libraries']
        ])

        # load the dilled heatmaps
        map_df = dill.load(open('dills/map_df_dynamicBW.dill'))
        map_df = map_df*multipliers
        # print map_df.head()

         # Boundary conditions for all maps (longitudes as x vals, latitudes as y vals)
        lonmin = -76.72
        lonmax = -76.52
        latmin = 39.19
        latmax = 39.38

        # number of points along each map edge
        # (total number of points is npts**2)
        npts = np.sqrt(len(map_df))
        x = np.linspace(lonmin, lonmax, npts)
        y = np.linspace(latmin, latmax, npts)
        X, Y = np.meshgrid(x, y, indexing='ij')

        # grid for heatmap calculation
        grid_points = np.vstack([X.ravel(), Y.ravel()])

        rec_map = map_df.sum(axis=1).values
        # print 'rec_map_vals:', rec_map[:10]

        MAP_THRESHHOLD = 0.85
        to_gmap = mapcalc_kde.produce_google_heatmap_points(rec_map, npts, grid_points, MAP_THRESHHOLD)

        return render_template(
            'index.html',
            to_gmap=to_gmap
        )

@app.route('/#recommendation', methods=['GET','POST'])
def recommendation():
    # on initial landing, show the default heatmap
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
        # user-defined weights for each map
        session=dict()
        session['crime'] = float(request.form['crime'])
        session['vacancy'] = float(request.form['vacancy'])
        session['grocery'] = float(request.form['grocery'])
        session['restaurant'] = float(request.form['restaurant'])
        session['schools'] = float(request.form['schools'])
        session['museums'] = float(request.form['museums'])
        session['parks'] = float(request.form['parks'])
        session['liquor'] = float(request.form['liquor'])
        session['libraries'] = float(request.form['libraries'])

        # weights as an array
        multipliers = np.array([
            session['crime'],
            session['vacancy'],
            session['grocery'],
            session['restaurant'],
            session['schools'],
            session['museums'],
            session['parks'],
            session['liquor'],
            session['libraries']
        ])

        # load the dilled heatmaps
        map_df = dill.load(open('dills/map_df_dynamicBW.dill'))
        map_df = map_df*multipliers
        # print map_df.head()

         # Boundary conditions for all maps
         # (longitudes as x vals, latitudes as y vals)
        lonmin = -76.72
        lonmax = -76.52
        latmin = 39.19
        latmax = 39.38

        # number of points along each map edge
        # (total number of points is npts**2)
        npts = np.sqrt(len(map_df))
        x = np.linspace(lonmin, lonmax, npts)
        y = np.linspace(latmin, latmax, npts)
        X, Y = np.meshgrid(x, y, indexing='ij')

        # grid for heatmap calculation
        grid_points = np.vstack([X.ravel(), Y.ravel()])

        rec_map = map_df.sum(axis=1).values
        # print 'rec_map_vals:', rec_map[:10]

        MAP_THRESHHOLD = 0.95
        to_gmap = mapcalc_kde.produce_google_heatmap_points(rec_map, npts, grid_points, MAP_THRESHHOLD)

        return render_template(
            'index.html',
            to_gmap=to_gmap
        )

if __name__ == '__main__':
    app.run(debug=False)
