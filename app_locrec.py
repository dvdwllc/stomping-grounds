import scripts.loc_rec

from flask import Flask, render_template, request, send_file
import numpy as np
import matplotlib.pyplot as plt

app_locrec = Flask(__name__)


@app_locrec.route('/', methods=['GET', 'POST'])
def index_locrec():
    if request.method == 'GET':
        return render_template('address_entry_locrec.html')
    else:
        requested_address = request.form['address']

        if len(requested_address) < 5:
            query_address = '3400 N. Charles St., Baltimore, MD'
        else:
            query_address = requested_address
        recommendation = \
            scripts.loc_rec.recommender(
                (query_address,
                 ('arrests', 'Offense', '87-Narcotics'),
                 ('groceries', 'type', 'Full Supermarket'),
                 'vacancies'
                 )
            )

        recommendation.compute_maps()

        # returns ideal address
        best_address = recommendation.recommend_location()

        return render_template(
            'recommendation_locrec.html',
            recommended_address=best_address,
            original_address=query_address
        )


@app_locrec.route('/img/<path:special_address>', methods=['GET'])
def img(special_address):
    if special_address == '':
        query_address = '3400 N. Charles St., Baltimore, MD'
    else:
        query_address = special_address

    recommendation = scripts.loc_rec.recommender(
        (query_address,
        ('arrests', 'Offense', '87-Narcotics'),
        ('groceries', 'type', 'Full Supermarket'),
        'vacancies')
    )

    recommendation.compute_maps()
    x, y, heatmap = recommendation.recommendation_map()

    print x[0]

    city_limits = np.array([(39.371582, -76.711036), (39.370668, -76.529172),
                            (39.209645, -76.529172), (39.196875, -76.549085),
                            (39.206985, -76.584790), (39.232519, -76.610883),
                            (39.278245, -76.710446), (39.371582, -76.711036)])


    plt.figure(figsize=(5, 5))
    plt.axis([x[0], x[-1], y[0], y[-1]])
    plt.pcolormesh(x, y, heatmap)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.plot(city_limits[:, 1], city_limits[:, 0], color='red')
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)

    plt.savefig('image.png', dpi=300)

    return send_file('image.png', mimetype='image/png')


if __name__ == '__main__':
    app_locrec.run(debug=True)
