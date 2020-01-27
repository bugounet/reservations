from django.db import models
from django.utils.timezone import now as tznow


class BookingQueryset(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.SCHEDULED)

    def for_user(self, user, **kwargs):
        kwargs.pop('owner', None)
        if user.is_staff:
            return self.filter(**kwargs)
        else:
            return self.filter(owner_id=user.pk, **kwargs)

    def past(self):
        return self.filter(end_datetime__lte=tznow())

    def ongoing(self):
        return self.filter(
            start_datetime__lte=tznow(),
            end_datetime__gte=tznow()
        )

    def upcoming(self):
        return self.filter(start_datetime__gte=tznow())

    def upcoming_and_current(self):
        return self.filter(end_datetime__gte=tznow())

    def overlapping_bookings(self, start, end):
        """ Get bookings that overap with given time interval.
        """
        return self.exclude(
            models.Q(
                start_datetime__gt=end,
                end_datetime__gt=end,
            ) |
            models.Q(
                start_datetime__lt=start,
                end_datetime__lt=start,
            )
        )
