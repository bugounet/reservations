from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Booking(models.Model):
    """ Booking: Resources reservations and rooms bookings.

    Only booking owner OR application admin can modify and view.
    Booking dates (start + end) are mandatory in order to restrict resources
    allocations in time. For recurring needs, create multiple bookings.
    """

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
