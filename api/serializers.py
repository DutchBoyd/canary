from models import Country, BadEvent, Index, Data, Risk, EstimatedRisk
from rest_framework import serializers
from django.conf import settings
from datetime import datetime

class CountrySerializer(serializers.ModelSerializer):
    trends = serializers.SerializerMethodField()
    
    def get_trends(self, obj):
        year = datetime.now().year
        trends = {}
        for index in Index.objects.all():
            trend = Data.objects.filter(index=index, country=obj, year__gte=year-settings.PAST_YEARS ).order_by('year').values_list('year', 'value')
            trends[index.name] = list(trend)
        return trends
    
    class Meta:
        model = Country
        fields = ('name', 'trends')

class CountryRiskSerializer(serializers.ModelSerializer):
    risk = serializers.SerializerMethodField()
    
    def get_risk( self, obj ):
        year = datetime.now().year
        try:
            risk = Risk.objects.get( country=obj, year=year )
        except Risk.DoesNotExist:
            risk = EstimatedRisk.objects.get( country=obj, year=year )
        return risk.value
    
    class Meta:
        model = Country
        fields = ('name', 'code', 'risk')

class BadEventSerializer(serializers.ModelSerializer):
    trends = serializers.SerializerMethodField()
    country_name = serializers.CharField(source="country.name")
    def get_trends(self, obj):
        trends = {}
        for index in Index.objects.all():
            trend = Data.objects.filter(index=index, country=obj.country, year__gte=obj.year-settings.PAST_YEARS, year__lte=obj.year ).order_by('year').values_list('year', 'value')
            trends[index.name] = list(trend)
        return trends
    
    class Meta:
        model = BadEvent 
        fields = ('name', 'trends', 'country_name', 'description', 'loss', 'year')
