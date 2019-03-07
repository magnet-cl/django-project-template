# django

# rest framework
from rest_framework import serializers

# models
from regions.models import Commune


class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = (
            'id',
            'name',
        )
