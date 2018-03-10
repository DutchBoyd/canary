# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render
import serializers
import models

# Create your views here.

class CountryViewSet( viewsets.ModelViewSet ):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()

class BadEventViewSet( viewsets.ModelViewSet ):
    serializer_class = serializers.BadEventSerializer
    queryset = models.BadEvent.objects.all()
    
