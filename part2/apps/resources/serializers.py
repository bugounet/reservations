from rest_framework import serializers

from apps.booking.serializers import BookingSerializer
from .models import Resource


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = [
            'location',
            'capacity',
            'label',
            'type',
            'upcoming_bookings',
            'id'
        ]

    upcoming_bookings = BookingSerializer(many=True, read_only=True)