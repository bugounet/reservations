from django.utils.timezone import now as tznow

from .exceptions import CannotCancelPastBooking, OverUsedResource


class BaseBookingExtension:
    def __init__(self, booking):
        self.booking = booking
        self.model = booking.__class__


class MetaInfo(BaseBookingExtension):

    def is_over(self):
        """ Is the booking end passed """
        return self.booking.end_datetime < tznow()

    def is_ongoing(self):
        """ Is the booking started and not ended yet."""
        return (
            self.booking.start_datetime <= tznow() < self.booking.end_datetime
        )

    def is_future(self):
        return self.booking.start_datetime > tznow()

    def upcoming_or_current(self):
        return self.booking.end_datetime > tznow()


class PreSaveChecks(BaseBookingExtension):

    def __init__(self, booking):
        super(PreSaveChecks, self).__init__(booking)
        self.resource = booking.resource

    def check_rules(self):
        is_new = self.booking.pk is None
        if is_new and self.exceeds_resource_capacity():
            raise OverUsedResource()

    def exceeds_resource_capacity(self):
        if self.resource.capacity is None:
            return False

        overlapping_boookings_on_same_resource = (
            self.model.objects
                .filter(resource_id=self.resource.pk)
                .active()
                .overlapping_bookings(
                    start=self.booking.start_datetime,
                    end=self.booking.end_datetime
                ).count()
        )

        return self.resource.capacity-1 < overlapping_boookings_on_same_resource


class BookingActions(BaseBookingExtension):

    def cancel(self):
        if self.booking.end_datetime < tznow():
            raise CannotCancelPastBooking()
        self.booking.status = self.model.CANCELLED
        self.booking.save(update_fields=['status'])
