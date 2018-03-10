from django.conf.urls import include, url
from rest_framework import routers
import views
# Two routes: travelplan and user
router = routers.DefaultRouter()
router.register(r'country', views.CountryViewSet, base_name='country')
router.register(r'badevent', views.BadEventViewSet, base_name='badevent')

urlpatterns = [
    url(r'^', include(router.urls)),
]

