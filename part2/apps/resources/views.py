from django.utils.timezone import now as tznow
from rest_framework import viewsets

from .permissions import IsOwnerOrAdmin
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.active()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if instance.end_datetime < tznow():
            raise Exception("Oops!")
        instance.actions.cancel()

    permission_classes = [IsOwnerOrAdmin]
