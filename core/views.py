from rest_framework import viewsets, permissions
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Sqrt, Power, Cos, Radians
from core.filters import RideFilter
from core.models import Ride
from core.serializers import RideSerializer


class IsAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class RideRestView(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    filterset_class = RideFilter
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = Ride.objects.all()

        query_params = self.request.query_params
        ordering = query_params.get('ordering')
        start_latitude, start_longitude = query_params.get('start_latitude'), query_params.get('start_longitude')

        if start_latitude and start_longitude:
            # Use 110.574 for kilometers
            # Use 69.1 for miles
            conversion_factor_miles_to_latitude = 69.1
            conversion_factor_degrees_to_radians = 57.3

            # Distance calculation is the distance between two points. This does not account the length
            # of the road between two points.
            # Reference: https://stackoverflow.com/a/5548877
            queryset = Ride.objects.annotate(
                distance=ExpressionWrapper(
                    Sqrt(
                        Power(conversion_factor_miles_to_latitude * (F("pickup_latitude") - start_latitude), 2) +
                        Power(conversion_factor_miles_to_latitude * (start_longitude - F("pickup_longitude")) * Cos(Radians(F("pickup_latitude")) / conversion_factor_degrees_to_radians), 2)
                    ),
                    output_field=FloatField(),
                )
            )

            # Add ordering if none is provided. Only applied when start_latitude and start_longitude is provided.
            if not ordering:
                queryset = queryset.order_by('distance')

        # TODO: Fix me. Will throw an exception when sorting by distance by no start_latitude/longitude is provided.
        if ordering:
            for order in ordering.split(','):
                queryset = queryset.order_by(order)

        return queryset
