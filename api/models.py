# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Country( models.Model ):
    """
    The Country in which things happen.
    """
    name = models.CharField(max_length=140, unique=True)
    code = models.CharField(max_length=2, default="")

class Asset( models.Model ):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=140)
    class Meta:
        unique_together = (('country', 'name'),)
        ordering = ['name']

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
    name = models.CharField(max_length=140, unique=True)

class Data( models.Model ):
    index   = models.ForeignKey(Index)
    country = models.ForeignKey(Country)
    year    = models.IntegerField()
    value   = models.FloatField()
    class Meta:
        unique_together = (('country', 'index', 'year'),)
        ordering = ['year']

class Risk( models.Model ):
    RISK_LEVEL = ( ('HIGH', 'High Risk'), ('MODERATE', 'Moderate Risk') )
    country = models.ForeignKey( Country )
    year = models.IntegerField()
    value = models.CharField(max_length=8, choices=RISK_LEVEL) 
    class Meta:
        unique_together = (('country', 'year'),)
        ordering = ['year']


class EstimatedRisk( models.Model ):
    RISK_LEVEL = ( ('HIGH', 'High Risk'), ('MODERATE', 'Moderate Risk') )
    country = models.ForeignKey( Country )
    year = models.IntegerField()
    value = models.CharField(max_length=8, choices=RISK_LEVEL) 
    class Meta:
        unique_together = (('country', 'year'),)
        ordering = ['year']

class BadEvent( models.Model ):
    name = models.CharField(max_length=140)
    description = models.TextField()
    loss = models.FloatField()
    year = models.IntegerField()
    country = models.ForeignKey(Country)
    class Meta:
        ordering = ['year', 'name']


