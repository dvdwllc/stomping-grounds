import scripts.loc_rec
from flask import Flask, render_template, request, send_file, session
import numpy as np
import matplotlib.pyplot as plt
from nocache import nocache

app_locrec = Flask(__name__)
# if you're reading this, don't look at the next line. It's SECRET ;)
app_locrec.config['SECRET_KEY'] = 'F#$6432fdsY$WTREWgfdassu54agfdsjyt;.,;gfd'

@app_locrec.route('/', methods=['GET', 'POST'])
@nocache
def index_locrec():
    if request.method == 'GET':
        return render_template('address_entry_locrec.html')
    else:
        # determine what to query
        session['address'] = request.form['address']
        session['arrests'] = 'arrests_data' in request.form
        session['grocery'] = 'grocery_data' in request.form
        session['vacancy'] = 'vacant_homes_data' in request.form
        session['top50'] = 'top50_data' in request.form

        # if all fields empty, show the default query
        if len(session['address']) == 0 and not (
                            session['arrests'] or
                            session['grocery'] or
                            session['vacancy'] or
                            session['top50']
        ):
            print 'Default Query!'
            query = ('22 N Green St., Baltimore, MD',
                     ('arrests', 'Offense', 'Unknown Offense'),
                     ('groceries', 'type', 'Full Supermarket'),
                     'vacancies'
                     )

            # build the recommendation map
            session['query'] = query
            recommendation = scripts.loc_rec.recommender(session['query'])
            recommendation.compute_maps()

            # get ideal address
            session['best_address'] = recommendation.recommend_location()

            # render the results page
            return render_template(
                'recommendation_locrec.html',
                recommended_address=session['best_address'],
                query=query
            )

        # User-defined query
        else:
            # build a properly formatted query
            query = []
            if len(session['address']) > 0:
                import geocoder
                try:
                    latlng = geocoder.arcgis(session['address']).latlng
                    if len(latlng) > 0:
                        query.append(session['address'])
                except:
                    pass
            if session['arrests']:
                query.append(('arrests', 'Offense', 'Unknown Offense'))
            if session['grocery']:
                query.append(('groceries', 'type', 'Full Supermarket'))
            if session['vacancy']:
                query.append('vacancies')
            if session['top50']:
                query.append('top50')

            # build the recommendation map
            session['query'] = query
            recommendation = scripts.loc_rec.recommender(session['query'])
            recommendation.compute_maps()

            # return ideal address
            session['best_address'] = recommendation.recommend_location()

            # render the results page
            return render_template(
                'recommendation_locrec.html',
                recommended_address=session['best_address']
            )


@app_locrec.route('/img', methods=['GET'])
@nocache
def img():
    query = session['query']
    recommendation = scripts.loc_rec.recommender(query)
    recommendation.compute_maps()
    x, y, heatmap = recommendation.recommendation_map()

    # Outline of Baltimore City
    city_limits = np.array([(39.371582, -76.711036), (39.370668, -76.529172),
                            (39.209645, -76.529172), (39.196875, -76.549085),
                            (39.206985, -76.584790), (39.232519, -76.610883),
                            (39.278245, -76.710446), (39.371582, -76.711036)])


    plt.figure(figsize=(5, 5))
    plt.title('Best location:\n%s' % session['best_address']).set_fontsize(12)
    plt.axis([x[0], x[-1], y[0], y[-1]])
    plt.pcolormesh(x, y, heatmap)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.plot(city_limits[:, 1], city_limits[:, 0], color='red', label='City limits')
    plt.legend(bbox_to_anchor=(0.05, 0.05), loc=3, borderaxespad=0., fancybox=True, framealpha=0.5)
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)

    plt.savefig('image.png', dpi=300)

    return send_file('image.png', mimetype='image/png')


if __name__ == '__main__':
    app_locrec.run(debug=False)
