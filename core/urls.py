from django.urls import path, include
from rest_framework import routers
from core.views import RideRestView

router = routers.SimpleRouter()
router.register('rides', RideRestView)

core_urls = [
    path('', include(router.urls))
]
