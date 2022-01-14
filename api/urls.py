# django
from django.urls import include
from django.urls import path

# rest framework
from rest_framework.routers import DefaultRouter

# views
from regions import viewsets as regions_views


# routers
router = DefaultRouter()

# regions
router.register(r'communes', regions_views.CommuneViewSet)


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
