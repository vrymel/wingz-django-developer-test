from rest_framework import serializers
from core.models import User, Ride


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'email', 'phone_number', 'first_name', 'last_name']


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id_ride', 'id_rider', 'rider', 'id_driver', 'driver', 'status', 'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude',
                  'pickup_time']

    rider = UserSerializer(source='id_rider', read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)
