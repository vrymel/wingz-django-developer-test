from rest_framework import serializers
from core.models import User, Ride, RideEvent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'email', 'phone_number', 'first_name', 'last_name']


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'id_ride', 'description', 'created_at', ]


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id_ride', 'id_rider', 'rider', 'id_driver', 'driver', 'status', 'pickup_latitude',
                  'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'ride_events', ]

    rider = UserSerializer(source='id_rider', read_only=True)
    id_rider = serializers.PrimaryKeyRelatedField(queryset=User.objects, write_only=True)

    driver = UserSerializer(source='id_driver', read_only=True)
    id_driver = serializers.PrimaryKeyRelatedField(queryset=User.objects, write_only=True)

    ride_events = RideEventSerializer(many=True, read_only=True)
