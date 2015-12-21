# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd

from django.db import migrations, transaction

from loc_rec.locations.models import Restaurant, Vacancy, GroceryStore


restaurants = pd.read_csv('clean_data/restaurant_list_GIS.csv', encoding='utf-8')
groceries = pd.read_csv('clean_data/grocerystore_list_GIS.csv')
vacancies = pd.read_csv('clean_data/vacancies_GIS.csv')

def get_datapoint_kwargs(entry):
    print entry
    return {
        'latitude': getattr(entry, 'Latitude'),
        'longitude': getattr(entry, 'Longitude')
    }


def migrate_restaurants(_restaurants):
    def get_kwargs(restaurant):
        kwargs = get_datapoint_kwargs(restaurant)
        kwargs.update({
            'name': getattr(restaurant, 'name'),
            'zip': getattr(restaurant, 'zipCode'),
            'address': getattr(restaurant, 'Location 1'),
        })

        return kwargs

    for i in range(len(restaurants)):
        _restaurant = _restaurants.iloc[i]
        kwargs = get_kwargs(_restaurant)
        Restaurant.objects.create(**kwargs)
        print str(i) + ' restaurant created'

def migrate_groceries(_groceries):
    def get_kwargs(grocery_store):
        kwargs = get_datapoint_kwargs(grocery_store)
        kwargs.update({
            'name': getattr(grocery_store, 'name'),
            'type': getattr(grocery_store, 'type'),
            'zip': getattr(grocery_store, 'zipCode'),
            'address': getattr(grocery_store, 'Location 1'),
        })

        return kwargs

    for i in range(len(_groceries)):
        _grocery_store = _groceries.iloc[i]
        kwargs = get_kwargs(_grocery_store)
        GroceryStore.objects.create(**kwargs)
        print str(i) + ' grocery store created'

def migrate_vacancies(_vacancies):
    for i in range(len(_vacancies)):
        _vacancy = _vacancies.iloc[i]
        kwargs = get_datapoint_kwargs(_vacancy)
        Vacancy.objects.create(**kwargs)
        print str(i) + ' vacancy created'


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0006_grocerystore_restaurant_vacancy'),
    ]


    def forward(self, schema_editor):
        with transaction.atomic():
            migrate_restaurants(restaurants)
            migrate_groceries(groceries)
            migrate_vacancies(vacancies)

    def reverse(self, schema_editor):
        Vacancy.objects.all().delete()
        GroceryStore.objects.all().delete()
        Restaurant.objects.all().delete()

        print 'Done!'

    operations = [
        migrations.RunPython(forward, reverse)
    ]
