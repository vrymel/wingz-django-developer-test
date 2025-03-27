from rest_framework import viewsets, permissions, pagination
from django.db.models import F, FloatField, ExpressionWrapper, Prefetch
from django.db.models.functions import Sqrt, Power, Cos, Radians
from django.utils.timezone import now
from datetime import timedelta
from core.filters import RideFilter
from core.models import Ride, RideEvent
from core.serializers import RideSerializer


# Uncomment to use Cursor based pagination. This will remove the need to query the total number of records.
# class CustomCursorPagination(pagination.CursorPagination):
#     ordering = 'pickup_time'
#     page_size = 25


class IsAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class RideRestView(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    filterset_class = RideFilter
    permission_classes = [IsAdmin]

    # Uncomment to use Cursor based pagination.
    # pagination_class = CustomCursorPagination

    def get_queryset(self):
        last_24_hours = now() - timedelta(hours=24)
        ride_events_queryset = RideEvent.objects.filter(created_at__gte=last_24_hours)

        queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
            Prefetch('ride_events', queryset=ride_events_queryset)
        )

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
            queryset = queryset.annotate(
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
