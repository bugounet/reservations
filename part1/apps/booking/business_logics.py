from django.utils.timezone import now as tznow


class MetaInfos():
    def __init__(self, booking):
        self.booking = booking

    def is_over(self):
        """ Is the booking end passed """
        return (self.booking.end_datetime < tznow())

    def is_ongoing(self):
        """ Is the booking started and not ended yet."""
        return (
            self.booking.start_datetime <= tznow() < self.booking.end_datetime
        )

class PreSaveChecks():
    def __init__(self, booking):
        self.booking = booking
        self.model = booking.__class__
        self.resource = booking.resource

    def exceeds_resource_capacity(self):
        if self.resource.capacity is None:
            return False

        overlapping_boookings_on_same_resource = (
            self.model.objects
                # note: if using status deletion, think of filtering active
                # bookings
                .filter(resource_id=self.resource.id)
                .overlapping_bookings(
                    start=self.booking.start_datetime,
                    end=self.booking.end_datetime
                ).count()
        )

        return self.resource.capacity-1 < overlapping_boookings_on_same_resource