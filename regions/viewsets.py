# django

# rest Framework
from rest_framework import viewsets

# models
from regions.models import Commune

# serializers
from regions.serializers import CommuneSerializer


class CommuneViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for communes.
    """
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer

    def get_queryset(self):
        """
        Allow optional filtering by `region_id` query parameter in the URL.
        """
        queryset = super(CommuneViewSet, self).get_queryset()

        region_id = self.request.query_params.get('regionId', None)
        if region_id is not None:
            queryset = queryset.filter(region_id=region_id)

        return queryset
