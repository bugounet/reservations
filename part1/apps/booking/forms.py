from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['title', 'start_datetime', 'end_datetime', 'resource']

    # Logic for raising error if end_date < start_date
    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")
        if end_datetime < start_datetime:
            raise forms.ValidationError(
                _('Invalid end date: %(value)s is before actual start'),
                params={'value': end_datetime.isoformat()},
            )
        return cleaned_data