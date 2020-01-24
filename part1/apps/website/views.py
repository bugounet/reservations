from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.timezone import now as tznow

from apps.booking.models import Booking
from apps.resources.models import Resource


@login_required
def index_view(request):
    """ Index view. This is reserved to authenticated users. Others are
    redirected to login screen.

    Index displays bookings and existing resources.
    """
    user = request.user
    return render(request, "website/index.html", {
        'user': user,
        'bookings': Booking.objects.for_user(user).filter(
            end_datetime__gte=tznow()
        ),
        'resources': Resource.objects.all(),
    })


def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def list_bookings_view(request):
    """ This view is in charge of view_bookings. You'll be able to using this form."""
    return render(request, 'website/view_bookings.html', {
        'user': request.user,
        'past_bookings':
            Booking.objects.for_user(request.user).past(),
        'upcoming_bookings':
            Booking.objects.for_user(request.user).upcoming_and_current()
    })
