from django.shortcuts import render
from rest_framework import viewsets
from core.models import Ride
from core.serializers import RideSerializer


# Create your views here.
class RideRestView(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    # return related RideEvents
    # return related Users (id_rider, id_driver
    # pagination
    # filter by ride status and rider email
