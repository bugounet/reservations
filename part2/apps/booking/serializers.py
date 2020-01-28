from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'owner',
            'resource',
            'start_datetime',
            'end_datetime',
            'title',
            'id',
        ]

    owner = serializers.CharField(source="owner.username")
