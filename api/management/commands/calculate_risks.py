from django.core.management.base import BaseCommand
from api.risk_classifier import RiskClassifier
from api.models import Country, EstimatedRisk
import csv
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        riskcls = RiskClassifier(train=True)
        data, country_order = riskcls.get_database_to_classify_data()
        X = data.as_matrix()
        classification_lasso, classification_enet = riskcls.classify(X)
        
        print type(classification_lasso)
        print type(classification_enet)
        
        for i, c in enumerate(country_order):
            value = 'HIGH' if classification_enet[i] > 0.75 else 'ACCEPTABLE'
            country = Country.objects.get(name=c)
            print country.name, value
            try:
                er = EstimatedRisk.objects.get(country=country, year=2018)
                er.value = value
                er.save()
            except EstimatedRisk.DoesNotExist:
                er = EstimatedRisk.objects.create(country=country, year=2018, value=value)
