from django.utils.timezone import now as tznow
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .exceptions import BRException
from .permissions import IsOwnerOrAdmin
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrAdmin]
    queryset = Booking.objects.active()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.actions.cancel()
        except BRException as e:
            raise ValidationError({'error': str(e)})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
