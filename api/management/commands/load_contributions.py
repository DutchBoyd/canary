from django.core.management.base import BaseCommand
from api.models import Country, DetailedInformation
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
                continue
            try:
                country = Country.objects.get(name=country_name)
            except Country.DoesNotExist:
                print "ne cname", country_name
                continue
            
            try:
                info = DetailedInformation.objects.get( country=country )
                info.contributions = row["Contributions"]
                info.losses = row["Losses"]
                info.description = row["Risks"]
                info.save()
            except DetailedInformation.DoesNotExist:
                try:
                    info = DetailedInformation.objects.create( country=country, contributions=float(row["Contributions"]), losses=float(row["Losses"]), description=row["Risks"])
                except ValueError:
                    print country.name, row
                    raise ValueError
            

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        loaddata( "countries/detailed.csv" )
    
