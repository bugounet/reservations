from datetime import timedelta
from random import randint
from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now as tznow

from apps.booking.business_logics import MetaInfos
from apps.booking.forms import BookingForm
from apps.booking.models import Booking
from apps.resources.models import Resource

class BookingSetupMixin():
    @classmethod
    def create_room_resource(cls, capacity=None):
        return Resource.objects.create(
            label="Room A",
            type="Conference-room",
            capacity=capacity
        )

    @classmethod
    def create_user(cls, name, admin=False):
        User = get_user_model()
        return User.objects.create(username=name, is_staff=admin)

    def create_booking(self, user, start=None, end=None):
        random_start = tznow() + timedelta(minutes=randint(100, 1000))
        random_end = random_start + timedelta(minutes=5)
        return Booking.objects.create(
            resource=self.room,
            owner=user,
            start_datetime=start or random_start,
            end_datetime=end or random_end
        )

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


class BookingManagerTestCase(BookingSetupMixin, TestCase):
    room = None
    user_1 = None
    user_2 = None
    user_admin = None

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

class ModelMetaInfosAndPropertiesTestCase(BookingSetupMixin, TestCase):
    room = None
    user_1 = None
    user_2 = None
    user_admin = None

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

    def test_model_get_aboslute_url(self):
        booking = self.create_booking(self.user_1)

        self.assertEqual(booking.get_absolute_url(), f'/booking/{booking.pk}')

    def test_meta_info_is_over_when_end_date_has_passed(self):
        mocked_booking = Mock()
        mocked_booking.end_datetime = tznow() - timedelta(hours=1)

        self.assertTrue(MetaInfos(mocked_booking).is_over())

    def test_meta_info_is_over_when_end_date_is_in_the_future(self):
        mocked_booking = Mock()
        mocked_booking.end_datetime = tznow()+timedelta(hours=1)

        self.assertFalse(MetaInfos(mocked_booking).is_over())

    def test_meta_infos_is_ongoing_when_started_but_not_ended(self):
        mocked_booking = Mock()
        mocked_booking.start_datetime = tznow() - timedelta(hours=1)
        mocked_booking.end_datetime = tznow() + timedelta(hours=1)

        self.assertTrue(MetaInfos(mocked_booking).is_ongoing())

    def test_meta_infos_is_ongoing_when_started_and_ended(self):
        mocked_booking = Mock()
        mocked_booking.start_datetime = tznow() - timedelta(hours=2)
        mocked_booking.end_datetime = tznow() - timedelta(hours=1)

        self.assertFalse(MetaInfos(mocked_booking).is_ongoing())

    def test_meta_infos_is_ongoing_when_not_started_yet(self):
        mocked_booking = Mock()
        mocked_booking.start_datetime = tznow() + timedelta(hours=1)
        mocked_booking.end_datetime = tznow() + timedelta(hours=2)

        self.assertFalse(MetaInfos(mocked_booking).is_ongoing())

class BookingFormTestCase(BookingSetupMixin, TestCase):
    room = None
    user_1 = None
    user_2 = None
    user_admin = None

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

    def test_end_date_before_Start_date_is_refused(self):
        booking = self.create_booking(self.user_1)

        form = BookingForm(instance=booking, data={
            'start_datetime': tznow()+timedelta(minutes=35),
            'end_datetime': tznow() + timedelta(minutes=10)
        })
        form.full_clean()

        with self.assertRaises(ValidationError):
            form.clean()

class ViewsTestCase(BookingSetupMixin, TestCase):
    room = None
    user_1 = None
    user_2 = None
    user_admin = None

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

    def test_display_owner_bookings(self):
        # assuming I'm logged in as booking owner
        booking = self.create_booking(self.user_1)
        self.client._login(booking.owner)

        # then when I access the booking details
        response = self.client.get(
            reverse('booking_details', kwargs={'pk': booking.pk})
        )

        # I succeed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, booking.title)
        self.assertQuerysetEqual(
            Booking.objects.filter(pk=response.context['booking'].pk),
            [repr(booking)]
        )

    def test_display_neighbourg_booking_fails_on_40(self):
        # assuming I'm not logged in as booking owner but someone else
        booking = self.create_booking(self.user_1)
        self.client._login(self.user_2)

        # then when I access the booking details
        response = self.client.get(
            reverse('booking_details', kwargs={'pk': booking.pk})
        )

        # I fail and no data is in contextdump
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(response.context.get('booking'))

    def test_display_others_booking_succeeds_as_admin(self):
        # assuming I'm logged in as admin
        booking = self.create_booking(self.user_1)
        self.client._login(self.user_admin)

        # then when I access the booking details
        response = self.client.get(
            reverse('booking_details', kwargs={'pk': booking.pk})
        )

        # I succeed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, booking.title)
        self.assertQuerysetEqual(
            Booking.objects.filter(pk=response.context['booking'].pk),
            [repr(booking)]
        )

class QuerySetTestCase(BookingSetupMixin, TestCase):
    room = None
    user_1 = None
    user_2 = None
    user_admin = None

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

    def test_past_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()-timedelta(minutes=30),
            end=tznow()-timedelta(minutes=60)
        )

        self.assertEqual(Booking.objects.past().first(), tested_booking)

    def test_upcoming_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()+timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.upcoming_and_current().first(),
            tested_booking
        )

    def test_current_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()-timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.upcoming_and_current().first(),
            tested_booking
        )

    def test_get_overlapping_left_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()+timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.overlapping_bookings(
                start=tznow()+timedelta(minutes=15),
                end=tznow()+timedelta(minutes=45)
            ).first(),
            tested_booking
        )

    def test_get_overlapping_right_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()+timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.overlapping_bookings(
                start=tznow() + timedelta(minutes=45),
                end=tznow() + timedelta(minutes=75)
            ).first(),
            tested_booking
        )

    def test_get_overlapping_middle_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()+timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.overlapping_bookings(
                start=tznow() + timedelta(minutes=35),
                end=tznow() + timedelta(minutes=55)
            ).first(),
            tested_booking
        )

    def test_get_overlapping_bigger_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()+timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.overlapping_bookings(
                start=tznow() + timedelta(minutes=15),
                end=tznow() + timedelta(minutes=75)
            ).first(),
            tested_booking
        )

    def test_get_overlapping_none_left_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()+timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.overlapping_bookings(
                start=tznow(),
                end=tznow() + timedelta(minutes=15)
            ).first(), None,
            tested_booking
        )

    def test_get_overlapping_none_right_bookings(self):
        tested_booking = self.create_booking(
            self.user_1,
            start=tznow()+timedelta(minutes=30),
            end=tznow()+timedelta(minutes=60)
        )

        self.assertEqual(
            Booking.objects.overlapping_bookings(
                start=tznow() + timedelta(minutes=75),
                end=tznow() + timedelta(minutes=90)
            ).first(), None,
            tested_booking
        )

class PreSaveChecksTestCase(BookingSetupMixin, TestCase):
    room = None
    user_1 = None
    user_2 = None
    user_admin = None

    @classmethod
    def setUpClass(cls):
        cls.user_1 = cls.create_user("1")
        cls.user_2 = cls.create_user("2")
        cls.user_admin = cls.create_user("admin", admin=True)

    @classmethod
    def tearDownClass(cls):
        cls.user_1.delete()
        cls.user_2.delete()
        cls.user_admin.delete()

    def test_book_twice_the_same_resource(self):
        self.room = self.create_room_resource(capacity=None)

        self.create_booking(self.user_1, tznow(), tznow()+timedelta(hours=1))
        self.create_booking(self.user_2, tznow(), tznow()+timedelta(hours=1))

    def test_book_twice_the_same_resource_when_it_has_only_one_spot(self):
        self.room = self.create_room_resource(capacity=1)

        self.create_booking(self.user_1, tznow(), tznow() + timedelta(hours=1))
        with self.assertRaises(ValidationError):
            self.create_booking(
                self.user_2, tznow(), tznow() + timedelta(hours=1)
            )
