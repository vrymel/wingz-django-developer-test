from django.shortcuts import render
from rest_framework import viewsets
from core.models import Ride
from core.serializers import RideSerializer


# Create your views here.
class RideRestView(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
