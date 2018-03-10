from django.core.management.base import BaseCommand
from api.models import Risk, Country
import csv
import os

def loaddata(f):
    with open(f) as datafile:
        data = csv.DictReader(datafile, delimiter=';')
        for row in data:
            try:
                country_name = unicode(row['Country'])
            except:
                print "cname", row['Country']
                raise Exception()
            print country_name
            country = Country.objects.get(name=country_name)
            Risk.objects.create(country=country, year=2017, value=row["2017"])
            Risk.objects.create(country=country, year=2018, value=row["2018"])

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        loaddata( "targets/risks.csv" )
    
