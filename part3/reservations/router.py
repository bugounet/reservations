from rest_framework import routers

from apps.booking.views import BookingViewSet
from apps.resources.views import ResourceViewSet

router = routers.DefaultRouter()
router.register('booking', BookingViewSet)
router.register('resource', ResourceViewSet)
