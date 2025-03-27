from rest_framework import serializers
from datetime import timedelta
from django.utils.timezone import now
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
                  'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'todays_ride_events', 'distance']

    rider = UserSerializer(source='id_rider', read_only=True)
    id_rider = serializers.PrimaryKeyRelatedField(queryset=User.objects, write_only=True)

    driver = UserSerializer(source='id_driver', read_only=True)
    id_driver = serializers.PrimaryKeyRelatedField(queryset=User.objects, write_only=True)

    todays_ride_events = serializers.SerializerMethodField()

    distance = serializers.SerializerMethodField()

    @staticmethod
    def get_distance(obj):
        if hasattr(obj, 'distance'):
            return obj.distance

        return None

    @staticmethod
    def get_todays_ride_events(obj):
        # Filter ride events to include only those from the last 24 hours
        last_24_hours = now() - timedelta(hours=24)
        events = RideEvent.objects.filter(id_ride=obj.id_ride, created_at__gte=last_24_hours)
        
        return RideEventSerializer(events, many=True).data
    