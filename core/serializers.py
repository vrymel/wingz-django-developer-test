from rest_framework import serializers
from core.models import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id_ride', 'pickup_latitude', 'pickup_longitude', ]
