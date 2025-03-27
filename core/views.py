from rest_framework import viewsets
from core.filters import RideFilter
from core.models import Ride
from core.serializers import RideSerializer


class RideRestView(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    filterset_class = RideFilter

    # return related RideEvents
    # pagination
