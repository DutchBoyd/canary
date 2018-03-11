# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render
import serializers
import models
from django.db.models import Q

# Create your views here.

class CountryViewSet( viewsets.ModelViewSet ):
    serializer_class = serializers.CountrySerializer
    def get_queryset(self):
        # filter by contains username
        code = self.request.query_params.get('code', None)
        
        if code is not None:
            return models.Country.objects.filter(code=code)
        else:
            return models.Country.objects.all()

class CountryRiskViewSet( viewsets.ModelViewSet ):
    serializer_class = serializers.CountryRiskSerializer
    queryset = models.Country.objects.all()

class BadEventViewSet( viewsets.ModelViewSet ):
    serializer_class = serializers.BadEventSerializer
    queryset = models.BadEvent.objects.all()
    
