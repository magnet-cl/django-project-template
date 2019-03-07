# django
from django.conf.urls import include
from django.conf.urls import url

# rest framework
from rest_framework.routers import DefaultRouter

# views
from regions import viewsets as regions_views


# routers
router = DefaultRouter()

# regions
router.register(r'communes', regions_views.CommuneViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
