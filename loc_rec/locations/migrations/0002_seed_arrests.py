# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd

from django.db import migrations, transaction

from loc_rec.locations.models import Arrest


ARRESTS = pd.read_csv('clean_data/arrests_GIS.csv')
LENGTH = len(ARRESTS)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    def forward(self, schema_editor):
        with transaction.atomic():
            for i in range(LENGTH):
                _arrest = ARRESTS.iloc[i].values

                Arrest.objects.create(
                    description=_arrest[1],
                    longitude=_arrest[2],
                    latitude=_arrest[3]
                )

                print str(i) + ' entry created'

            print 'Done!'

    def reverse(self, schema_editor):
        Arrest.objects.all().delete()

    operations = [
        migrations.RunPython(forward, reverse)
    ]
