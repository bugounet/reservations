from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.booking.business_logics import PreSaveChecks
from .queryset import BookingQueryset
from .business_logics import MetaInfos


class Booking(models.Model):
    """ Booking: Resources reservations and rooms bookings.

    Only booking owner OR application admin can modify and view.
    Booking dates (start + end) are mandatory in order to restrict resources
    allocations in time. For recurring needs, create multiple bookings.
    """

    objects = BookingQueryset.as_manager()

    owner = models.ForeignKey(
        to='auth.User',
        related_name="bookings",
        verbose_name=_("User"),
        help_text=_("User owning this"),
        on_delete=models.CASCADE,
    )
    resource = models.ForeignKey(
        verbose_name=_("Resource"),
        related_name="bookings",
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

    def save(self, *args, **kwargs):
        is_new = self.id is None
        if is_new and PreSaveChecks(self).exceeds_resource_capacity():
            raise ValidationError(
                _("Can't save booking. Resource is overused.")
            )
        return super(Booking, self).save(*args, **kwargs)
