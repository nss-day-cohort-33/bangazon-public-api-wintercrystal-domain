from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from kennywoodapi.models import *
from kennywoodapi.views import register_user, login_user
from kennywoodapi.views import ParkAreas, Attractions

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'parkareas', ParkAreas, 'parkarea')
router.register(r'attractions', Attractions, 'attraction')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth$', obtain_auth_token),
    url(r'^api-auth$', include('rest_framework.urls', namespace='rest_framework')),
]
