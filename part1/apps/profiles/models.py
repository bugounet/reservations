from django.db import models
import pytz


class UserPreference(models.Model):
    """ Store user preferences.

    Preferences are stored in a serparate table to protect user sensitive
    data in case of SQL injection. Even if SQL injections are hard to achieve
    in django's ORM, you're never 100% safe.
    """

    # In order to reduce dev time for the test I choose not to create a
    # project-level user model but to rely on django's basic user model
    # This has been often discussed over the web that the good practice is to
    # have your own models even if django's model fits the need at project
    # start.
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='preferences'
    )

    # Preferred timezone is not using django-timezone-field library (not
    # allowed in test scenario) but in prod I would have used it.
    _preferred_timezone = models.CharField(
        max_length=255,
        default='Europe/Paris',
        # source: https://stackoverflow.com/a/45867250 --> create pytz choices
        choices=tuple(zip(pytz.all_timezones, pytz.all_timezones)),
    )

    @property
    def preferred_timezone(self):
        return pytz.timezone(self._preferred_timezone)

    @preferred_timezone.setter
    def _set_preferred_timezone(self, new_timezone):
        self._preferred_timezone = new_timezone.zone

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.user_id} - {str(self.user)} preferences"

from .hooks import *