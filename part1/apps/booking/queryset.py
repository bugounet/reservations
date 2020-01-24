from django.db import models
from django.utils.timezone import now as tznow


class BookingQueryset(models.QuerySet):
    def for_user(self, user, **kwargs):
        kwargs.pop('owner', None)
        if user.is_staff:
            return self.filter(**kwargs)
        else:
            return self.filter(owner_id=user.id, **kwargs)

    def past(self):
        return self.filter(end_datetime__lte=tznow())

    def upcoming_and_current(self):
        return self.filter(end_datetime__gte=tznow())

    def overlapping_bookings(self, start, end):
        """ Get bookings that overap with given time interval.
        """
        return self.exclude(
            models.Q(
                start_datetime__gte=end,
                end_datetime__gte=end,
            ) |
            models.Q(
                start_datetime__lte=start,
                end_datetime__lte=start,
            )
        )
