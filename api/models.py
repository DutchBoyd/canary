# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Country( models.Model ):
    """
    The Country in which things happen.
    """
    name = models.CharField(max_length=140)

class Asset( models.Model ):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=140)

class Contributions( models.Model ):
    asset = models.ForeignKey(Asset)
    category = models.CharField(max_length=140)
    subcategory = models.CharField(max_length=140)
    year = models.IntegerField()
    amount = models.FloatField()

class Index( models.Model ):
    """
    The index where things are reflected.
    """
    name = models.CharField(max_length=140)

class Data( models.Model ):
    index   = models.ForeignKey(Index)
    country = models.ForeignKey(Country)
    value   = models.FloatField()

class BadEvent( models.Model ):
    name = models.CharField(max_length=140)
    description = models.TextField()
    loss = models.FloatField()
    year = models.IntegerField()
    country = models.ForeignKey(Country)
