from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Booking
from .forms import BookingForm


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    allow_empty = True
    template_name = 'booking/booking_list.html'

    def get_queryset(self, *args, **kwargs):
        return Booking.objects.for_user(self.request.user).order_by(
            '-start_datetime'
        )


class BookingDetailsView(LoginRequiredMixin, UpdateView):
    model = Booking
    template_name = 'booking/booking_detail.html'
    form_class = BookingForm
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.for_user(self.request.user)


class BookingCreationView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'booking/booking_create.html'
    form_class = BookingForm
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.for_user(self.request.user)


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
