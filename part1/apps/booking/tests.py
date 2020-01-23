from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now as tznow

from apps.booking.models import Booking
from apps.resources.models import Resource


class BookingCascadeRemovalTestCase(TestCase):
    """ Make sure the bookings are always removed if their owner is removed
    or if the resource is removed.
    """
    tests_count = 0

    def create_booking(self):
        User = get_user_model()
        owner = User.objects.create(username="toto")
        room = Resource.objects.create(label="Room A", type="Conference-room")
        test_number = BookingCascadeRemovalTestCase.tests_count
        BookingCascadeRemovalTestCase.tests_count += 1
        return Booking.objects.create(
            owner=owner,
            resource=room,
            start_datetime=tznow(),
            end_datetime=tznow()+timedelta(hours=1),
            title=f"Booking number {test_number}"
        )

    def test_auto_remove_on_user_deletion(self):
        # assuming
        booking = self.create_booking()

        # when
        booking.owner.delete()

        # Then
        self.assertFalse(Booking.objects.filter(pk=booking.pk).exists())

    def test_auto_remove_on_resource_deletion(self):
        # assuming
        booking = self.create_booking()

        # when
        booking.resource.delete()

        # Then
        self.assertFalse(Booking.objects.filter(pk=booking.pk).exists())
