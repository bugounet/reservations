from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from apps.booking.models import Booking
from apps.resources.models import Resource


def get_bookings(user_id, is_admin=False):
    if is_admin:
        return Booking.objects.all()
    else:
        return Booking.objects.filter(owner_id=user_id)


def get_resources():
    return Resource.objects.all()


@login_required
def index_view(request):
    user = request.user
    return render(request, "website/index.html", {
        'user': user,
        'bookings': get_bookings(user.id, is_admin=user.is_staff),
        'resources': get_resources(),
    })


def logout_view(request):
    logout(request)
    return redirect('login')
