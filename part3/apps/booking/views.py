from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .exceptions import BRException
from .forms import BookingForm
from .models import Booking
from .permissions import IsOwnerOrAdmin
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrAdmin]
    queryset = Booking.objects.active().order_by('start_datetime')
    serializer_class = BookingSerializer

    def get_queryset(self):
        return (
            Booking.objects
                .active()
                .for_user(self.request.user)
                .order_by('start_datetime')
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.actions.cancel()
        except BRException as e:
            raise ValidationError({'error': str(e)})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

class BookingListView(LoginRequiredMixin, ListView):
    """ This list allows you to view your bookings.

    You can add a filter on bookings dates to view past, ongoing or upcoming:

    GET /bookings?timeline=[past/ongoing/future]
    """
    model = Booking
    allow_empty = True
    paginate_by = 10
    template_name = 'booking/booking_list.html'

    def get_queryset(self, *args, **kwargs):
        bookings_queryset = Booking.objects.for_user(
            self.request.user).active().order_by(
            '-start_datetime'
        )
        timeline = self.request.GET.get('timeline', None)
        if timeline not in ['past', 'ongoing', 'future']:
            return bookings_queryset
        # else:
        if timeline == 'past':
            return bookings_queryset.past()
        elif timeline == 'ongoing':
            return bookings_queryset.ongoing()
        else:
            return bookings_queryset.upcoming()


class BookingDetailsView(LoginRequiredMixin, UpdateView):
    model = Booking
    template_name = 'booking/booking_detail.html'
    form_class = BookingForm
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.for_user(self.request.user).active()


class BookingCreationView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'booking/booking_create.html'
    form_class = BookingForm
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.for_user(self.request.user).active()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BookingDeletionView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/booking_delete.html'
    context_object_name = 'booking'

    def get_success_url(self):
        return reverse('bookings_list')

    def get_queryset(self):
        return (
            Booking.objects
            .for_user(self.request.user)
            .active()
            .upcoming_and_current()
        )

    def delete(self, request, *args, **kwargs):
        """Override delete action to change object status instead of calling the
        "delete" function on model.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = 'cancelled'
        self.object.save(update_fields=['status'])
        return HttpResponseRedirect(success_url)

