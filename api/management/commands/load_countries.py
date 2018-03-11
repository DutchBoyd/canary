from django.core.management.base import BaseCommand
from api.models import Country
import csv
import os

def loaddata(f):
    with open(f) as datafile:
        data = csv.DictReader(datafile, delimiter=';')
        for row in data:
            try:
                country_name = unicode(row['name'])
            except:
                print "cname", row['name']
                continue
            try:
                country = Country.objects.get(name=country_name)
            except Country.DoesNotExist:
                print "ne cname", country_name
                continue
            
            country.code = row["alpha-2"]
            country.save()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        loaddata( "countries/codes.csv" )
    
