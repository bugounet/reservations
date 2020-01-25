import pytz
from django import forms
from django.utils.translation import ugettext_lazy as _
from pytz import UnknownTimeZoneError

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['title', 'start_datetime', 'end_datetime', 'resource']

    start_datetime = forms.DateTimeField(
        help_text=_("Format yyyy-mm-dd hh:mm:ss"),
        required=True,
        localize=True
    )
    end_datetime = forms.DateTimeField(
        help_text=_("Format yyyy-mm-dd hh:mm:ss"),
        required=True,
        localize=True
    )

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")


        if not (end_datetime and start_datetime):
            raise forms.ValidationError(
                _("Missing start or end date. Both are required.")
            )

        if end_datetime < start_datetime:
            raise forms.ValidationError(
                _('Invalid end date: %(value)s is before actual start'),
                params={'value': end_datetime.isoformat()},
            )

        # Use form's input timezone to cast given datetime to UTC
        requester_timezone = self.get_requester_timezone_from_data()
        cleaned_data['start_datetime'] = self.to_utc(
            requester_timezone, start_datetime
        )
        cleaned_data['end_datetime'] = self.to_utc(
            requester_timezone, end_datetime
        )

        return cleaned_data

    def get_requester_timezone_from_data(self):
        """ Return timezone filled in input form. or UTC in case of failure.
        """
        try:
            return pytz.timezone(self.data.get('timezone', 'UTC'))
        except UnknownTimeZoneError:
            return pytz.utc

    def to_utc(self, src_timezone, date):
        naive_date = date.replace(tzinfo=None)
        return src_timezone.localize(naive_date).astimezone(pytz.utc)
