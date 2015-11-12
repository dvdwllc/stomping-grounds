import scripts.loc_rec

from flask import Flask,render_template,request,redirect
app_locrec = Flask(__name__)

app_locrec.vars=dict()

app_locrec.default_queries = (('arrests', 'Offense', '87-Narcotics'), 
                              ('groceries', 'type', 'Full Supermarket'),
                              'vacancies')


@app_locrec.route('/index_locrec',methods=['GET','POST'])
def index_locrec():
    if request.method == 'GET':
        print 'GET'
        return render_template('address_entry_locrec.html')
    else:
        app_locrec.vars['address'] = request.form['address']
        
        with open('query.txt', 'w') as outfile:
            outfile.write(str(app_locrec.vars['address'])+'\n')
        
        return redirect('/main_locrec')
 
@app_locrec.route('/main_locrec',methods=['GET','POST'])
def main_locrec():
    recommendation = \
        scripts.loc_rec.recommender((app_locrec.vars['address'],
                                     ('arrests', 'Offense', '87-Narcotics'),
                                     ('groceries', 'type', 'Full Supermarket'),
                                     'vacancies'))
        
    recommendation.compute_maps()
                                     
    # returns ideal address and saves a plot 'recommendation.png'                           
    best_address = recommendation.recommend_location_map()
    
    return render_template('recommendation_locrec.html',
                            address=best_address)
                            
if __name__ == '__main__':
    app_locrec.run(debug=True)