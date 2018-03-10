# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from models import Country, Asset, Index, Data, BadEvent
import json
# Create your tests here.
class TestApp(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api(self):
            
        # Create countries.
        countries = ['Colombia', 'Brazil', 'Mexico']
        for country in countries:
            Country.objects.create(name=country)
        # Create assets.
        assets = { 'Colombia': ['Cartagena', 'Medellin'], 'Brazil': {'Rio'}, 'Mexico': ['Ixtapa', 'Mexico'] }
        for country in Country.objects.all():
            for asset in assets[country.name]:
                Asset.objects.create(country=country, name=asset)
        # Create indices
        indices = ['health', 'education', 'employment']
        for index in indices:
            Index.objects.create( name=index )
        i = 1
        j = 1
        for country in Country.objects.all():
            i += 1
            for index in Index.objects.all():
                j += 1
                for year in range(2008, 2018):
                    value = float(year+j)/i
                    Data.objects.create(country=country, index=index, year=year, value=value)
        
        bad_events = [('Colosa', 'Consulta popular.', 100000, 2015, 'Colombia'), ('Iguazu', 'Water felt over the mine.', 200000, 2010, 'Brazil')]
        for name, description, loss, year, country_name in bad_events:
            country = Country.objects.get(name=country_name)
            BadEvent.objects.create( country=country, name=name, description=description, loss=loss, year=year )

        result = self.client.get('/api/country/')
        self.assertEqual(len(result.data), 3)
        self.assertEqual(len(result.data[0]['trends']['education']), 10)
        result = self.client.get('/api/badevent/')
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0]['country_name'], 'Brazil') 
        self.assertEqual(len(result.data[0]['trends']['health']), 3)
