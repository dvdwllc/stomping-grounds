# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd

from django.db import migrations, transaction

from loc_rec.locations.models import School


SCHOOLS = pd.read_csv('clean_data/school_list_GIS.csv')
LENGTH = len(SCHOOLS)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0004_auto_20151221_2210'),
    ]

    def forward(self, schema_editor):
        with transaction.atomic():
            for i in range(LENGTH):
                _school = SCHOOLS.iloc[i].values
                print _school

                kwargs={
                    'number': _school[1],
                    'name': _school[2],
                    'address': _school[3],
                    'zip': _school[4],
                    'phone': _school[5],
                    'lead_first_name': _school[6],
                    'lead_last_name': _school[7],
                    'grades_served': _school[8],
                    'longitude': _school[9],
                    'latitude': _school[10],
                }
                print kwargs

                School.objects.create(**kwargs)

                print str(i) + ' School entry created'

            print 'Done!'

    def reverse(self, schema_editor):
        School.objects.all().delete()

    operations = [
        migrations.RunPython(forward, reverse)
    ]
