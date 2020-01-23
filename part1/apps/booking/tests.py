from datetime import timedelta
from random import randint

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


class BookingManagerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.room = cls.create_room_resource()
        cls.user_1 = cls.create_user("1")
        cls.user_2 = cls.create_user("2")
        cls.user_admin = cls.create_user("admin", admin=True)

    @classmethod
    def tearDownClass(cls):
        cls.room.delete()
        cls.user_1.delete()
        cls.user_2.delete()
        cls.user_admin.delete()

    @classmethod
    def create_room_resource(cls):
        return Resource.objects.create(label="Room A", type="Conference-room")

    @classmethod
    def create_user(cls, name, admin=False):
        User = get_user_model()
        return User.objects.create(username=name, is_staff=admin)

    def create_booking(self, user):
        random_start = tznow()+timedelta(minutes=randint(100, 1000))
        end = random_start+timedelta(minutes=5)
        return Booking.objects.create(
            resource=self.room,
            owner=user,
            start_datetime=random_start,
            end_datetime=end
        )

    def test_booking_for_user_returns_all_bookings_when_admin(self):
        # assuming you have 1 booking on user 1 and 2 bookings on user 2
        self.create_booking(self.user_1)
        self.create_booking(self.user_2)
        self.create_booking(self.user_2)

        self.assertEqual(Booking.objects.for_user(self.user_admin).count(), 3)

    def test_booking_for_user_only_features_my_bookings(self):
        # assuming you have 1 booking on user 1 and 2 bookings on user 2
        self.create_booking(self.user_1)
        self.create_booking(self.user_2)
        self.create_booking(self.user_2)

        self.assertEqual(Booking.objects.for_user(self.user_1).count(), 1)
        self.assertEqual(
            Booking.objects.for_user(self.user_1)[0].owner_id,
            self.user_1.id
        )
