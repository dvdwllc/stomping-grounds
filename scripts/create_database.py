import pandas as pd
from sqlalchemy import create_engine

arrests = pd.read_csv('clean_data/arrests_GIS.csv')
schools = pd.read_csv('clean_data/school_list_GIS.csv')
restaurants = pd.read_csv('clean_data/restaurant_list_GIS.csv', encoding='Latin-1')
groceries = pd.read_csv('clean_data/grocerystore_list_GIS.csv')
vacancies = pd.read_csv('clean_data/vacancies_GIS.csv')

disk_engine = create_engine('sqlite:///baltimore.db')
# Initializes database with filename baltimore.db in current directory

arrests.to_sql('arrests', disk_engine)
schools.to_sql('schools', disk_engine)
restaurants.to_sql('restaurants', disk_engine)
groceries.to_sql('groceries', disk_engine)
vacancies.to_sql('vacancies', disk_engine)
