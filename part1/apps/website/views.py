from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from apps.booking.models import Booking
from apps.resources.models import Resource


def get_bookings(user):
    return Booking.objects.for_user(user)


def get_resources():
    return Resource.objects.all()


@login_required
def index_view(request):
    """ Index view. This is reserved to authenticated users. Others are
    redirected to login screen.

    Index displays bookings and existing resources.
    """
    user = request.user
    return render(request, "website/index.html", {
        'user': user,
        'bookings': get_bookings(user),
        'resources': get_resources(),
    })


def logout_view(request):
    logout(request)
    return redirect('login')
