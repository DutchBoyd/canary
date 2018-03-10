from models import Country, BadEvent
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
    trends = serializers.SerializerMethodField()
    ok = serializers.SerializerMethodField()
    class Meta:
        model = Country
        fields = ('name', 'trends', 'ok')

class BadEventSerializer(serializers.ModelSerializer):
    trends = serializers.SerializerMethodField()
    class Meta:
        model = BadEvent 
        fields = ('name', 'trends', 'country.name', 'description', 'loss', 'year')

