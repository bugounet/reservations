from django.db import models
from django.utils.translation import ugettext_lazy as _


class Resource(models.Model):
    """ Resource is an thing you can book or allocate for a given amount of
    time and for a certain number of persons.

    No field indexed at the moment since I don't know how users would search
    resources.
    """

    # Unknown at dev time: what format location is in. Using CharField for
    # flexibiliy. Until I get answers I'll consider location is a string like
    # 'First floor, left door, desk 7, next to boby'
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Resource location")
    )

    # Capacity: assuming it's the max number of people using the Resource at
    # a given time. If unset, this Resource isn't limited to X persons (like
    # a very big screen). To ease this implementation, I consider the number
    # of persons is equal to the number of bookings. I know one person
    # could create two bookings on the same time-slot. But for a test,
    # let's reduce complexity.
    capacity = models.PositiveSmallIntegerField(
        verbose_name=_("Capacity"),
        null=True,
        blank=True,
        help_text=_("Resource capacity in number of persons.")
    )

    # Resource name
    label = models.CharField(
        verbose_name=_("Label"),
        max_length=255,
    )

    # Resource type. No list defined here. I'm assuming this could be
    # something like "desk", "room", "screen" etc.
    type = models.CharField(
        verbose_name=_("Type"),
        max_length=255,
        help_text=_("Resource type. eg: desk, room, screen, pen, parking spot")
    )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.label}"

    def upcoming_bookings(self):
        return self.bookings.upcoming_and_current()
