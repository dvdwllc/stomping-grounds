import scripts.loc_rec

from flask import Flask, render_template, request, redirect

app_locrec = Flask(__name__)


@app_locrec.route('/index_locrec', methods=['GET', 'POST'])
def index_locrec():
	if request.method == 'GET':
		print 'GET'
		return render_template('address_entry_locrec.html')
	else:
		special_address = request.form['address']

		recommendation = \
			scripts.loc_rec.recommender(
				(special_address,
				('arrests', 'Offense', '87-Narcotics'),
				('groceries', 'type', 'Full Supermarket'),
				'vacancies')
			)

		recommendation.compute_maps()

		# returns ideal address and saves a plot 'recommendation.png'
		best_address = recommendation.recommend_location_map()

		with open('all_queries.txt', 'w') as outfile:
			outfile.write(special_address + '\n')

		return render_template(
			'recommendation_locrec.html',
		    address=best_address,
			image='static/recommendation.png'
		)


if __name__ == '__main__':
	app_locrec.run(debug=False)
