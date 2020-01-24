from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Booking


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['title', 'start_datetime', 'end_datetime', 'resource']

    def clean_end_datetime(self, value):
        if self.model.start_datetime >= value:
            ValidationError(
                _('Invalid end date: %(value)s is before actual start'),
                params={'value': value.isoformat()},
            )
