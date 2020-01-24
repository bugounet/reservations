from django.db import models
from django.utils.timezone import now as tznow
from django.utils.translation import ugettext_lazy as _

from .business_logics import MetaInfos


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


class Booking(models.Model):
    """ Booking: Resources reservations and rooms bookings.

    Only booking owner OR application admin can modify and view.
    Booking dates (start + end) are mandatory in order to restrict resources
    allocations in time. For recurring needs, create multiple bookings.
    """

    objects = BookingQueryset.as_manager()

    owner = models.ForeignKey(
        to='auth.User',
        verbose_name=_("User"),
        help_text=_("User owning this"),
        on_delete=models.CASCADE,
    )
    resource = models.ForeignKey(
        verbose_name=_("Resource"),
        to='resources.Resource',
        on_delete=models.CASCADE,
        help_text=_("Booked resource.")
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Booking start date & time"),
        help_text=_("Beginning of the booking")
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("Booking end date & time"),
        help_text=_("End of usage date and time")
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Name of the event/reservation. max 250 chars.")
    )

    @property
    def meta_infos(self):
        return MetaInfos(self)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('booking_details', kwargs={'pk': self.pk})