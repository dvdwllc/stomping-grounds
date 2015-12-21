from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class DataPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Arrest(DataPoint):
    description = models.CharField(max_length=1000)


class School(DataPoint):
    number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    lead_first_name = models.CharField(max_length=100, null=True, blank=True)
    lead_last_name = models.CharField(max_length=100, null=True, blank=True)
    grades_served = models.CharField(max_length=200, null=True, blank=True)

