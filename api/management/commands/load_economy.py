from django.core.management.base import BaseCommand
from api.models import Data, Country, Index
import csv
import os
def loaddata(index, f):
    index_name = index
    try:
        index = Index.objects.get(name=index_name)
        Data.objects.filter(index=index).delete()
    except Index.DoesNotExist:
        index = Index.objects.create(name=index_name)

    with open(f) as datafile:
        data = csv.DictReader(datafile, delimiter=';')
        for row in data:
            try:
                country_name = unicode(row['Country Name'])
            except:
                print "cname", row['Country Name']
                raise Exception()
            try:
                country = Country.objects.get(name=country_name)
            except Country.DoesNotExist:
                country = Country.objects.create(name=country_name)
            for fname in data.fieldnames:
                if not fname in ['Country Name', 'Region']:
                    try:
                        year = int(fname)
                    except ValueError:
                        continue
                    try:
                        rec = Data.objects.get(country=country, index=index, year=year)
                        continue
                    except Data.DoesNotExist:
                        pass

                    try:
                        Data.objects.create(country=country, index=index, year=year, value=float(row[fname]))
                    except ValueError:
                        pass
 
class Command(BaseCommand):
#    def add_arguments(self, parser):
#        parser.add_argument('index', type=str)
#        parser.add_argument('file', type=str)


   def handle(self, *args, **kwargs):
        files = os.listdir("economy")
        names = map( lambda f: f.split(".")[0], files )
        files = map( lambda f: os.path.join("economy", f), files )
        for n, f in zip( names, files ):
            loaddata( n, f )
